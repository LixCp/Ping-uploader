# main.py

from telethon import TelegramClient,events
import asyncio
import logging
from config import api_hash,api_id,bot_token
from plugins.start import start_message,handel_url
from database.db import setup_database

app = TelegramClient('uploader',api_id=api_id,api_hash=api_hash).start(bot_token=bot_token)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)



def main():
    logger.info('BotISStarted...')
    setup_database()

    app.add_event_handler(start_message,events.NewMessage(pattern='^/[Ss][Tt][Aa][Rr][Tt]'))
    app.add_event_handler(handel_url,events.NewMessage(pattern=r'https?://[^\s/$.?#].[^\s]*'))

    app.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
    