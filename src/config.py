# config.py - Bridge's configuration file. Sets-up a few things
# Copyright (C) 2023 Amritpal Singh
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
Qmaxsize: int = 25
message_queue: asyncio.Queue = asyncio.Queue(Qmaxsize)

# misc variables
channels: dict = {}  # dictionary to dump for channels
large_upload_to_discord: bool = False
small_uploads_only: bool = True
