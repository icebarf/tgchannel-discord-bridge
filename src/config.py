from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio

# setup logging configuration
import logging
from datetime import datetime
time_now = datetime.now()
time_str = time_now.strftime("%d_%m_%Y_%H_%M_%S")
log_handler = logging.basicConfig(filename= time_str + "_telegram_discord.log", format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

# login data and channels to work with
api_id = None
api_hash = None
telegram_channel_id = None
discord_channel_id = None
telegram_login_string = None
discord_token = None

import json
with open("login.json", "r", encoding="utf-8") as file:
      json_data = json.load(file)
      api_id = json_data["api_id"]
      api_hash = json_data["api_hash"]
      telegram_channel_id = json_data["telegram_channel_id"]
      discord_channel_id = json_data["discord_channel_id"]
      telegram_login_string = json_data["telegram_login_string"]
      discord_token = json_data["discord_token"]

# Set up the telegram client
LocalTelegramClient = TelegramClient(StringSession(telegram_login_string), api_id, api_hash, sequential_updates=True)

# Set up the message queue
message_queue = asyncio.Queue(maxsize=10)