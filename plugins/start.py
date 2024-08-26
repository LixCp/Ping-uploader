# plugins/start.py

import os
from database.db import create_user
from .download import download_file
from .upload import uploadfile
from .yt_dlp import is_yt_dlp_supported,yt_dlp_download
from assets.utils import get_filename

async def start_message (event):
    create_user(event.sender_id)
    await event.reply('سلام به ربات خوش آمدید یک لینک ارسال کنید تا آن را در تلگرام آپلود کنم.')

async def handel_url(event):
    url = event.message.message
    last_message = await event.reply('لینک دریافت شد لطفا منتظر بمانید')
    if not is_yt_dlp_supported(url):

        file_name = get_filename(url)
        if not file_name :
            await event.reply('اجازه دانلود این نوع فایل داده نشده است.')
            return
        
        file_path = os.path.join('downloads',file_name)
        download_sucsess = await download_file(url,file_path,last_message)
    else:
        download_sucsess = await yt_dlp_download(url,event,filepath=file_path,last_message=last_message)
        
    if not download_sucsess :
        return
    await uploadfile(event,last_message=last_message,filepath=file_path)