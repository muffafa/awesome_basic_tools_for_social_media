#to disable ssl error temporarily
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from pytube import YouTube
import os

# url input from user
yt = YouTube(
	str(input("Enter the URL of the video you want to download: \n>> ")))

# extract only audio
video = yt.streams.filter(only_audio=True).first()

# check for destination to save file
print("Enter the destination (leave blank for dowloads directory for current destination)")
destination = str(input(">> ")) or './downloads'

# download the file
out_file = video.download(output_path=destination)

# save the file
base, ext = os.path.splitext(out_file)
new_file = base + '.mp3'
os.rename(out_file, new_file)

# result of success
print(yt.title + " has been successfully downloaded.")
