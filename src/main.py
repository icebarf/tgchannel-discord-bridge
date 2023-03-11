import json
from telethon import TelegramClient, events
from telethon import sync
from telethon.tl.functions.help import GetTermsOfServiceUpdateRequest

import logging
from datetime import datetime
time_now = datetime.now()
time_str = time_now.strftime("%d_%m_%Y_%H_%M_%S")
logging.basicConfig(filename= time_str + "_telegram_discord.log", format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

api_id = None
api_hash = None
name = None

with open("login.json", "r", encoding="utf-8") as file:
      json_data = json.load(file)
      api_id = json_data["api_id"]
      api_hash = json_data["api_hash"]
      name = json_data["name"]


Client = TelegramClient('anon', api_id, api_hash)

async def main():
    me = await Client.get_me()
    print(me.stringify())

    username = me.username
    print(username)
    print(me.phone)

    async for dialog in Client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)


    await Client.send_message('me', "Kida Mitra!")
    #await Client.send_message(-1001434290216, )
    await Client.send_message(-1001434290216, "Joined Group a while ago.")
    await Client.send_message(-1001434290216, "Testing successful")
    await Client.send_message("inf_user", "DM Testing successful")

    message = await Client.send_message(-1001434290216,
                                        "**Bold**, __italics__,"
                                        " `code`, and a"
                                        " link to a [website](https://rdseed.in/)"
                                        , link_preview=False)
    print(message)
    await message.reply("Reply test successful")

    #await Client.send_file(-1001434290216,
    #                       "/home/ice/Pictures/Wallpapers/lakeside_house.jpg")
    await Client.send_message(-1001434290216, "All tests successful")

with Client:
     Client.loop.run_until_complete(main())