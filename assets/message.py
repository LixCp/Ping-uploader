# assets/message.py

def DOWNLOAD_PROGRESS_MESSAGE(progress_bar, progress_percentage, current_size_mb, total_size_mb, speed_kb_s, time_left_formatted):
    return (
        f"درحال دانلود:\n\n"
        f"`{progress_bar} {progress_percentage:.2f}%`\n"
        f"دانلود شده: \n`{current_size_mb:.2f} MB of {total_size_mb:.2f} MB`\n"
        f"سرعت دانلود: \n`{speed_kb_s:.2f} KB/s`\n"
        f"زمان باقی مانده: `{time_left_formatted}`"
    )
