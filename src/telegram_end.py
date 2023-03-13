from config import logging
from telethon import events
from telethon.tl.custom.file import File
from telethon.tl.custom.message import Message
import asyncio
import config
import os
import shutil

telegram_channels: list = []
discord_channels: list = []  # associated discord channel
# the reason both are separate and not a dictionary is
# because the key or discord channel associated with the
# value(s) or telegram channel(s) is not unique i.e
# for a single discord channel, there are multiple
# telegram channels


def server_copy(file: str, /) -> str:
    shutil.copy(file, config.media_location)
    os.remove(file)
    return config.media_url + file


def load_channels() -> None:
    global telegram_channels
    for key, value in config.channels.items():
        if isinstance(value, list):
            for item in value:
                telegram_channels.append(int(item))
                discord_channels.append(int(key))
        else:
            telegram_channels.append(int(value))
            discord_channels.append(int(key))


async def get_and_queue_message(event: Message, text_prefix: str):
    if event.chat_id in telegram_channels:
        discord_text = "**" + text_prefix + "**:\n" + event.text
        media: File = event.file
        file = None
        if media is not None:
            file = await event.download_media()
            logging.info("telegram: Downloaded media file at : " + file)
            if media.size >= (7.5 * 1024 * 1024):
                url = server_copy(file)
                file = None
                discord_text = discord_text + \
                    "\nMedia too large. Here's a direct link: " + url

        item = [discord_channels[telegram_channels.index(
            event.chat_id)], discord_text, file]
        await config.message_queue.put(item)
        logging.info("telegram: %s", event.text)
        logging.info("telegram: exiting the message_event_handler()")


@config.LocalTelegramClient.on(events.NewMessage)
async def message_event_handler(event: Message):
    logging.info("telegram: Message handler was called")
    logging.info("telegram: Chat Id: " + str(event.chat_id))
    logging.info(
        "telegram: received these channels from discord: {}".format(telegram_channels))
    reply_message = await event.get_reply_message()
    update_str = "Update"
    if reply_message is not None:
        await get_and_queue_message(reply_message, "Old " + update_str)
        update_str = "Reply to old " + update_str
    await get_and_queue_message(event, update_str)


async def telegram_main():
    me = await config.LocalTelegramClient.get_me()
    logging.info("telegram: Telegram User information: %s", me.stringify())

    username = me.username
    logging.info("telegram: %s", username)
    logging.info("telegram: %s", me.phone)

    async for dialog in config.LocalTelegramClient.iter_dialogs():
        string = dialog.name + ' has ID ' + str(dialog.id)
    logging.info("telegram: %s", string)

    while True:
        await asyncio.sleep(1)
