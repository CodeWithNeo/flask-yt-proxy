cat > app.py << EOL
from flask import Flask, Response
import requests
from yt_dlp import YoutubeDL
import time

app = Flask(__name__)

YOUTUBE_URL = "https://www.youtube.com/watch?v=QoUkQUq57LA "
COOKIES_FILE = 'cookies.txt'
LAST_FETCH = {'url': None, 'time': 0}
CACHE_TTL = 60  # Cache for 60 seconds to reduce load

def get_m3u8_url():
    try:
        current_time = time.time()
        if LAST_FETCH['url'] and (current_time - LAST_FETCH['time']) < CACHE_TTL:
            return LAST_FETCH['url']

        ydl_opts = {
            'format': '96',
            'quiet': True,
            'no_warnings': True,
            'forceurl': True,
            'cookiefile': COOKIES_FILE,
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(YOUTUBE_URL, download=False)
            m3u8_url = info.get('url')
            LAST_FETCH.update({'url': m3u8_url, 'time': current_time})
            return m3u8_url
    except Exception as e:
        print("Error fetching m3u8 URL:", e)
        return None

@app.route("/")
def home():
    return "ARY Digital Proxy is Live!"

@app.route("/ary-digital.m3u8")
def proxy():
    m3u8_url = get_m3u8_url()
    if not m3u8_url:
        return "Failed to fetch stream", 500

    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(m3u8_url, headers=headers, stream=True)

    return Response(
        r.iter_content(chunk_size=4096),
        content_type=r.headers.get('Content-Type', 'application/vnd.apple.mpegurl')
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
EOL
