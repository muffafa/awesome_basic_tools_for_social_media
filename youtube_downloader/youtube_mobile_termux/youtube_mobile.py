import os, subprocess
from pytubefix import YouTube

yt = YouTube(input("Video linki: "))
videos = yt.streams.filter(adaptive=True, only_video=True).order_by("resolution").desc()
for i, s in enumerate(videos):
    print(f"{i}: {s.resolution} {s.fps}fps {s.mime_type}")
sec = input("Numara seç (Enter = en yüksek): ")
v = videos[int(sec)] if sec else videos[0]
a = yt.streams.get_audio_only()
dest = input("Kayıt yeri (Enter = /sdcard/Download): ") or "/sdcard/Download"
print("Video indiriliyor...")
vf = v.download(output_path=dest, filename="tmp_video")
print("Ses indiriliyor...")
af = a.download(output_path=dest, filename="tmp_audio")
name = "".join(c for c in yt.title if c not in '\\/:*?"<>|')
out = os.path.join(dest, name + ".mp4")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vf, "-i", af, "-c", "copy", out], check=True)
os.remove(vf); os.remove(af)
print("Bitti:", out)
