# assets/utils.py

import requests
import magic
import os

def generate_progress_bar(progress, length=10):
    filled_length = int(length * progress)
    bar = '⬛️' * filled_length + '⬜️' * (length - filled_length)
    return bar

def format_time(seconds):
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        return f"{int(seconds // 60)}m {int(seconds % 60)}s"
    else:
        return f"{int(seconds // 3600)}h {int((seconds % 3600) // 60)}m {int(seconds % 60)}s"

def get_filename(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Range': 'bytes=0-4095'  # Request the first 4KB of the file
        }
        response = requests.get(url, headers=headers, stream=True, allow_redirects=True)
        response.raise_for_status()
        final_url = response.url
        filename = os.path.basename(final_url)
        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(response.content)
        mime_to_extension = {
            'video/mp4': 'mp4',
            'video/x-matroska': 'mkv',
            'application/zip': 'zip',
            'application/vnd.rar': 'rar',
            'audio/mpeg': 'mp3',
            'application/vnd.android.package-archive': 'apk',
            'application/x-msdownload': 'exe',
            'image/jpeg': 'jpg',
            'image/png': 'png',
            'application/pdf': 'pdf',
            'application/octet-stream': 'bin',
            'application/octet-stream': 'dat' 
            # Add more mappings as needed
        }
        if file_type not in mime_to_extension:
            return False
        file_extension = mime_to_extension[file_type]
        if file_extension and not filename.lower().endswith(f".{file_extension}"):
            formatted_filename = f"{filename}.{file_extension}"
        else:
            formatted_filename = filename

        return formatted_filename
    
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {e}"
    except requests.exceptions.RequestException as e:
        return f"Request Error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"