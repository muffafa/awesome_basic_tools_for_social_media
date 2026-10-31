# YouTube HD downloader for Android (Termux)

Downloads 1080p+ by fetching video and audio separately and merging them with ffmpeg.

1. Install Termux from F-Droid (Play Store version is outdated)
2. `pkg update && pkg install python git nodejs ffmpeg -y`
3. `termux-setup-storage` (allow storage access)
4. `pip install aiohttp && pip install pytubefix --no-deps`
5. Point pytubefix to Termux's Node.js (its nodejs wheel can't build on Android):

~~~
SP=$(python -c "import site;print(site.getsitepackages()[0])")
mkdir -p $SP/nodejs_wheel && touch $SP/nodejs_wheel/__init__.py
echo "ROOT_DIR='$PREFIX'" > $SP/nodejs_wheel/executable.py
~~~

6. `python youtube_mobile.py`

Files are saved to `/sdcard/Download` (the phone's internal storage) by default.
