from telethon.sync import TelegramClient
from telethon.sessions import StringSession

import json
api_id = None
api_hash = None

with open ("login.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)
    api_id = json_data['api_id']
    api_hash = json_data['api_hash']

with TelegramClient(StringSession(), api_id, api_hash) as Client:
    print(Client.session.save())