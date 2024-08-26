# plugins/upload.py

import os
import time
from datetime import datetime, timedelta
from assets.utils import generate_progress_bar, format_time

async def uploadfile(event, last_message, filepath):
    total_size = os.path.getsize(filepath)
    start_time = time.time()
    last_update_time = datetime.now()

    async def progress(current, total):
        nonlocal last_update_time
        elapsed_time = time.time() - start_time
        progress_ratio = current / total_size
        speed = current / elapsed_time if elapsed_time > 0 else 0
        time_left = (total_size - current) / speed if speed > 0 else 0
        progress_bar = generate_progress_bar(progress_ratio)
        if datetime.now() - last_update_time > timedelta(seconds=3):
            await last_message.edit(
                f"درحال آپلود:\n\n`{progress_bar} {progress_ratio * 100:.2f}%`\n"
                f"آپلود شده: \n`{current/1024/1024:.2f} MB of {total_size/1024/1024:.2f} MB`\n"
                f"سرعت آپلود: \n`{speed/1024:.2f} KB/s`\n"
                f"زمان باقی مانده: `{format_time(time_left)}`"
            )
            last_update_time = datetime.now()

    try:
        await last_message.edit("آپلود فایل شروع شده است. لطفا منتظر بمانید...")

        await event.client.send_file(
            event.chat_id, 
            file=filepath, 
            caption="فایل شما با موفقیت آپلود شد.", 
            progress_callback=progress
        )

        await last_message.delete()
        await event.reply("فایل با موفقیت آپلود شد.")

        os.remove(filepath)

    except Exception as e:
        await event.reply("خطایی در هنگام آپلود فایل رخ داد. لطفا دوباره تلاش کنید.")
        print(f"Error uploading file: {e}")
