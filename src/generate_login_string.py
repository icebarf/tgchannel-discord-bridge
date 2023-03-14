# generate_login_string.py - Generates a telegram user login string for use with bridge
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

from telethon.sync import TelegramClient
from telethon.sessions import StringSession

import json
api_id = None
api_hash = None

with open("login.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)
    api_id = json_data['api_id']
    api_hash = json_data['api_hash']

with TelegramClient(StringSession(), api_id, api_hash) as Client:
    print(Client.session.save())
