from config import LocalTelegramClient
from telegram_end import telegram_main

import os

if os.name != "nt":
    import uvloop
    uvloop.install()

def telegram_launcher():
    with LocalTelegramClient:
        LocalTelegramClient.loop.run_until_complete(telegram_main())

telegram_launcher()