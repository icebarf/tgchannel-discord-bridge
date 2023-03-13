import json
from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio

# setup logging configuration
import logging
from datetime import datetime
time_now: datetime = datetime.now()
time_str: str = time_now.strftime("%d_%m_%Y_%H_%M_%S")
log_handler: logging.Logger = logging.basicConfig(filename=time_str + "_telegram_discord.log", format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                                                  level=logging.INFO)
# login data and channels to work with
api_id: int = None
api_hash: str = None
telegram_login_string: str = None
discord_token: str = None
media_location: str = None
media_url: str = None
discord_admins: list = None

with open("login.json", "r", encoding="utf-8") as file:
    json_data: dict = json.load(file)
    api_id = json_data["api_id"]
    api_hash = json_data["api_hash"]
    telegram_login_string = json_data["telegram_login_string"]
    discord_token = json_data["discord_token"]
    media_location = json_data["media_location"]
    media_url = json_data["media_url"]
    discord_admins = json_data["discord_admins"]
    file.close()

# Set up the telegram client
LocalTelegramClient: TelegramClient = TelegramClient(StringSession(
    telegram_login_string), api_id, api_hash, sequential_updates=True)

# Set up the message queue
message_queue: asyncio.Queue = asyncio.Queue(maxsize=25)

channels: dict = {}
