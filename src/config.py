from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.help import GetTermsOfServiceUpdateRequest

import logging
from datetime import datetime
time_now = datetime.now()
time_str = time_now.strftime("%d_%m_%Y_%H_%M_%S")
logging.basicConfig(filename= time_str + "_telegram_discord.log", format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

api_id = None
api_hash = None
channel_id = None
telegram_login_string = None

import json
with open("login.json", "r", encoding="utf-8") as file:
      json_data = json.load(file)
      api_id = json_data["api_id"]
      api_hash = json_data["api_hash"]
      channel_id = json_data["channel_id"]
      telegram_login_string = json_data["telegram_login_string"]

LocalTelegramClient = TelegramClient(StringSession(telegram_login_string), api_id, api_hash, sequential_updates=True)
