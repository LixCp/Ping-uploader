# plugins/download.py

import aiofiles
import aiohttp
import time
import asyncio
from datetime import datetime, timedelta
from assets.utils import generate_progress_bar, format_time
from assets.message import DOWNLOAD_PROGRESS_MESSAGE

async def download_file(url, filepath, last_message):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=300)) as response:  # Increased timeout to 300 seconds
                if response.status == 200:
                    total_size = int(response.headers.get('content-length', 0))
                    chunk_size = 8192
                    downloaded_size = 0
                    start_time = time.time()
                    last_update_time = datetime.now()

                    async with aiofiles.open(filepath, "wb") as file:
                        async for chunk in response.content.iter_chunked(chunk_size):
                            await file.write(chunk)
                            downloaded_size += len(chunk)
                            elapsed_time = time.time() - start_time
                            progress = downloaded_size / total_size if total_size else 0
                            speed = downloaded_size / elapsed_time if elapsed_time > 0 else 0
                            time_left = (total_size - downloaded_size) / speed if speed > 0 else 0
                            progress_bar = generate_progress_bar(progress)

                            # Convert bytes to MB and speed to KB/s
                            current_size_mb = downloaded_size / 1024 / 1024
                            total_size_mb = total_size / 1024 / 1024
                            speed_kb_s = speed / 1024

                            # Update the progress every 3 seconds
                            if datetime.now() - last_update_time > timedelta(seconds=3):
                                await last_message.edit(
                                    DOWNLOAD_PROGRESS_MESSAGE(
                                        progress_bar,
                                        progress * 100,
                                        current_size_mb,
                                        total_size_mb,
                                        speed_kb_s,
                                        format_time(time_left)
                                    )
                                )
                                last_update_time = datetime.now()

                    await last_message.edit('دانلود با موفقیت انجام شد!')
                    print(f"Download complete: {filepath}")
                    return True
                else:
                    raise Exception(f"Failed to download file, status code: {response.status}")
    except aiohttp.ClientError as e:
        await last_message.edit("خطایی در ارتباط با سرور رخ داد. لطفا دوباره تلاش کنید.")
        print(f"Client error occurred: {e}")
    except asyncio.TimeoutError:
        await last_message.edit("زمان دانلود به پایان رسید. لطفا دوباره تلاش کنید.")
        print("Download timed out.")
    except Exception as e:
        await last_message.edit("خطایی در هنگام دانلود فایل رخ داد. لطفا دوباره تلاش کنید.")
        print(f"Unexpected error: {e}")
