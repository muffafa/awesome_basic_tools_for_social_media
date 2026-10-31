import os, sys, time, shutil, socket, subprocess, http.client

# Sadece IPv4 kullan: bazi VPN'ler IPv6 trafigini tasimiyor
_gai = socket.getaddrinfo
socket.getaddrinfo = lambda h, p, f=0, *a, **k: _gai(h, p, socket.AF_INET, *a, **k)

import pytubefix.request
from pytubefix import YouTube, extract
from pytubefix import exceptions as ex

# 2 MB parcalar halinde indir: ilerleme her 2 MB'da guncellenir
pytubefix.request.default_range_size = 2 * 1024 * 1024

# Bazi VPN'ler Python'un buyuk sayfa okumasini yarida kesiyor; o zaman sayfayi curl ile cek
_python_get = pytubefix.request.get


def _guvenli_get(url, extra_headers=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
    try:
        return _python_get(url, extra_headers, timeout)
    except (http.client.IncompleteRead, ConnectionError):
        komut = ["curl", "-4", "-sSL", "--fail", "--retry", "3",
                 "-H", "User-Agent: Mozilla/5.0", "-H", "accept-language: en-US,en"]
        for k, v in (extra_headers or {}).items():
            komut += ["-H", f"{k}: {v}"]
        sonuc = subprocess.run(komut + [url], capture_output=True)
        if sonuc.returncode != 0:
            raise ConnectionError(sonuc.stderr.decode(errors="replace").strip())
        return sonuc.stdout.decode("utf-8")


pytubefix.request.get = _guvenli_get

GIRIS = any(a.strip("-—–") == "giris" for a in sys.argv[1:])
KOMUT = f"python {sys.argv[0]} --giris"
t0 = time.time()


def sure(sn):
    sn = int(sn)
    return f"{sn // 60}:{sn % 60:02d}"


def ilerleme(stream, chunk, kalan):
    toplam = stream.filesize or 1
    inen = toplam - kalan
    gecen = max(time.time() - t0, 0.001)
    hiz = inen / gecen
    yuzde = inen * 100 / toplam
    dolu = int(yuzde / 10)
    satir = (f"{'█' * dolu}{'░' * (10 - dolu)} {yuzde:3.0f}% "
             f"{inen / 1048576:.0f}/{toplam / 1048576:.0f}MB "
             f"{hiz / 1048576:.1f}MB/s ~{sure(kalan / hiz) if hiz else '?'}")
    genislik = shutil.get_terminal_size((45, 20)).columns - 1
    sys.stdout.write("\r" + satir[:genislik].ljust(genislik))
    sys.stdout.flush()


def indir(stream, hedef, ad, baslik):
    global t0
    print(f"{baslik} ({stream.filesize_mb:.1f} MB)")
    t0 = time.time()
    yol = stream.download(output_path=hedef, filename=ad, timeout=30, max_retries=5)
    print(f"\n  tamamlandı, {sure(time.time() - t0)} sürdü")
    return yol


def aciklama(hata, neden):
    durumlar = [
        (ex.VideoPrivate, "Video gizli; sadece sahibinin izin verdiği hesaplar izleyebilir."),
        (ex.VideoRemovedByUploader, "Video, sahibi tarafından silinmiş."),
        (ex.AccountTerminated, "Videonun kanalı YouTube tarafından kapatılmış."),
        (ex.VideoRemovedByYouTubeForViolatingTOS, "Video, kural ihlali nedeniyle YouTube tarafından kaldırılmış."),
        (ex.MembersOnly, "Video sadece kanal üyelerine açık."),
        (ex.VideoBlockedByCopyright, "Video, telif hakkı nedeniyle senin ülkende engelli."),
        (ex.VideoRegionBlocked, "Video sahibi bu videoyu senin ülkende yayınlamamış."),
        (ex.AgeRestrictedError, "Yaş sınırlı video; giriş gerekiyor: " + KOMUT),
        (ex.AgeCheckRequiredError, "Yaş sınırlı video; giriş gerekiyor: " + KOMUT),
        (ex.AgeCheckRequiredAccountError, "Yaş sınırlı video; giriş gerekiyor: " + KOMUT),
        (ex.BotDetection, "YouTube bu bağlantıyı bot sandı (VPN'lerde sık olur). "
                          "Başka bir VPN sunucusu dene ya da giriş yaparak çalıştır: " + KOMUT),
        (ex.LiveStreamError, "Bu bir canlı yayın; yayın bitince tekrar dene."),
    ]
    for sinif, mesaj in durumlar:
        if isinstance(hata, sinif):
            return mesaj
    n = neden.lower()
    if any(k in n for k in ("legal", "government", "yasal", "hükümet", "mahkeme")):
        return "Video, yasal bir şikâyet veya resmi talep nedeniyle senin ülkende erişime kapatılmış."
    if any(k in n for k in ("country", "ülke")):
        return "Video senin ülkende kullanılamıyor."
    return "Kesin sebep anlaşılamadı; yukarıdaki YouTube mesajına bak ya da linki YouTube uygulamasında aç."


url = input("Video linki: ")
print("Video bilgileri alınıyor...")
if GIRIS:
    print("Giriş modu: ilk seferde ekrana çıkan kodu google.com/device adresine gir.")

# Bot kontrolune takilirsa sirayla diger YouTube istemcilerini dene
istemciler = [None] if GIRIS else [None, "WEB", "TV", "IOS", "ANDROID_VR"]
AG_HATALARI = (http.client.HTTPException, OSError)  # baglanti kopmasi, DNS, zaman asimi


def bilgi_al(ayar):
    """Kalite listesini al; baglanti koparsa ayni istemciyle 3 kez dene."""
    global yt
    for deneme in range(3):
        yt = YouTube(url, **ayar)
        try:
            return yt.streams.filter(adaptive=True, only_video=True).order_by("resolution").desc()
        except AG_HATALARI:
            if deneme == 2:
                raise
            print(f"  bağlantı koptu, tekrar deneniyor ({deneme + 2}/3)...")
            time.sleep(2)


yt, videos, hata = None, None, None
for ist in istemciler:
    ayar = {"on_progress_callback": ilerleme}
    if GIRIS:
        ayar.update(use_oauth=True, allow_oauth_cache=True)
    elif ist:
        ayar["client"] = ist
    try:
        videos = bilgi_al(ayar)
        break
    except (ex.BotDetection, ex.LoginRequired, ex.PoTokenRequired) as h:
        hata = h
        print(f"  {ist or 'varsayılan'} istemcisi bot kontrolüne takıldı, başkası deneniyor...")
    except ex.VideoUnavailable as h:
        hata = h
        break
    except AG_HATALARI as h:
        hata = h
        print(f"  {ist or 'varsayılan'} istemcisiyle bağlanılamadı, başkası deneniyor...")

if videos is None:
    if isinstance(hata, AG_HATALARI):
        print("\nYouTube'a bağlanılamadı. İnternetini veya VPN bağlantını kontrol edip tekrar dene.")
        sys.exit(1)
    try:
        _, nedenler = extract.playability_status(yt.vid_info)
        neden = " ".join(str(r) for r in nedenler if r)
    except Exception:
        neden = ""
    print("\nBu video indirilemiyor.")
    print("YouTube'un mesajı:", neden or "(mesaj yok)")
    print("Durum:", aciklama(hata, neden))
    sys.exit(1)

for i, s in enumerate(videos):
    print(f"{i}: {s.resolution} {s.fps}fps {s.mime_type} {s.filesize_mb:.0f}MB")
sec = input("Numara seç (Enter = en yüksek): ")
v = videos[int(sec)] if sec else videos[0]
a = yt.streams.get_audio_only()
dest = input("Kayıt yeri (Enter = /sdcard/Download): ") or "/sdcard/Download"

vf = indir(v, dest, "tmp_video", f"[1/3] Video: {v.resolution}")
af = indir(a, dest, "tmp_audio", "[2/3] Ses")

print("[3/3] Birleştiriliyor...")
name = "".join(c for c in yt.title if c not in '\\/:*?"<>|')
out = os.path.join(dest, name + ".mp4")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vf, "-i", af, "-c", "copy", out], check=True)
os.remove(vf); os.remove(af)
print("Bitti:", out)
