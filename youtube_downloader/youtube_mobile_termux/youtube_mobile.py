import os, sys, time, shutil, subprocess
import pytubefix.request
from pytubefix import YouTube

# 2 MB parcalar halinde indir: ilerleme her 2 MB'da guncellenir
pytubefix.request.default_range_size = 2 * 1024 * 1024

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
    yol = stream.download(output_path=hedef, filename=ad)
    print(f"\n  tamamlandı, {sure(time.time() - t0)} sürdü")
    return yol


yt = YouTube(input("Video linki: "), on_progress_callback=ilerleme)
print("Video bilgileri alınıyor...")
videos = yt.streams.filter(adaptive=True, only_video=True).order_by("resolution").desc()
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
