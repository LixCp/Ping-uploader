# plugins/yt_dlp.py

import yt_dlp
import asyncio
from time import time
from assets.utils import generate_progress_bar, format_time
from assets.message import DOWNLOAD_PROGRESS_MESSAGE

# Check if the URL is supported by yt-dlp
def is_yt_dlp_supported(url):
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'simulate': True,  # Only check URL without downloading
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return True
    except Exception:
        return False

# Download file using yt-dlp
async def yt_dlp_download(url, event, filepath, last_message):
    loop = asyncio.get_event_loop()
    last_edit_time = time()  # Track the last edit time
    edit_interval = 1.0  # Minimum time interval between edits (in seconds)
    
    def progress_hook(d):
        nonlocal last_edit_time
        
        if d['status'] == 'downloading':
            total_size = d.get('total_bytes', 0)
            downloaded_size = d.get('downloaded_bytes', 0)
            speed = d.get('speed', 0)
            eta = d.get('eta', 0)
            
            # Handle None values and ensure valid types
            total_size = total_size or 0
            downloaded_size = downloaded_size or 0
            speed = speed or 0
            eta = eta or 0
            
            progress = downloaded_size / total_size if total_size > 0 else 0
            current_size_mb = downloaded_size / 1024 / 1024
            total_size_mb = total_size / 1024 / 1024
            speed_kb_s = speed / 1024

            # Throttle the message edits based on the edit_interval
            current_time = time()
            if current_time - last_edit_time >= edit_interval:
                last_edit_time = current_time
                loop.call_soon_threadsafe(lambda: asyncio.ensure_future(
                    last_message.edit(
                        DOWNLOAD_PROGRESS_MESSAGE(
                            generate_progress_bar(progress),
                            progress * 100,
                            current_size_mb,
                            total_size_mb,
                            speed_kb_s,
                            format_time(eta)
                        )
                    )
                ))

    ydl_opts = {
        'outtmpl': filepath,
        'progress_hooks': [progress_hook],
        'quiet': True,           # Suppress all console output
        'noprogress': True,      # Disable progress bar in the console
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await loop.run_in_executor(None, ydl.download, [url])
        await last_message.edit('دانلود با موفقیت انجام شد!')
        return True
    except Exception as e:
        await last_message.edit("خطایی در هنگام دانلود فایل رخ داد. لطفا دوباره تلاش کنید.")
        print(f"Error downloading with yt-dlp: {e}")
        return False
