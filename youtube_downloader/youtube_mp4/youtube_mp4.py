#to disable ssl error temporarily
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from pytube import YouTube

answer = str(input("Would you like to install highest resolution or want to show all options? (Y/n):"))

# url input from user
yt = YouTube(
	str(input("Enter the URL of the video you want to download: \n>> ")))

if(answer == "n"):
    # get all videos
    streams = yt.streams.filter(file_extension='mp4')

    for stream in streams:
        # print itag, resolution and codec format of Mp4 streams
        print(f"Video itag : {stream.itag} Resolution : {stream.resolution} VCodec : {stream.codecs[0]}")
 
    # enter the itag value of resolution on which you want to download the video
    input_itag = input("Enter itag Value : \n>> ")
    # get video using itag vale
    video = yt.streams.get_by_itag(input_itag)

video = yt.streams.get_highest_resolution()
    
# print resolution and codec format of highest resolution mp4 stream
print(f"Video Resolution : {video.resolution} VCodec : {video.codecs[0]}")

# check for destination to save file
print("Enter the destination (leave blank for dowloads directory for current destination)")
destination = str(input(">> ")) or './downloads'

print("Video is Downloading as",yt.title+".mp4")

# download the file
video.download(output_path=destination)

# result of success
print(yt.title + " has been successfully downloaded.")
