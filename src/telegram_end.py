# main.py - Bridge's backend part
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

from config import logging
from telethon import events
from telethon.tl.custom.file import File
from telethon.tl.custom.message import Message
import asyncio
import config
import myutility
import os
import shutil

media_max: int = 100 * 1024 * 1024
media_min: int = 7.9 * 1024 * 1024
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
    global discord_channels
    telegram_channels = []
    discord_channels = []
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
        discord_text: str = "**" + text_prefix + "**:\n" + event.text
        media: File = event.file
        media_size: int = None
        file: str = None
        if media is not None:
            media_size = media.size
            if config.small_uploads_only:
                if media_size <= media_min:
                    file = await event.download_media()
                    logging.info(
                        "telegram: Downloaded media file at : " + file)
                else:
                    discord_text = discord_text + \
                        "\nMedia attachment too large, only small uploads are enabled."
            elif config.large_upload_to_discord:
                if media_size <= media_max:
                    file = await event.download_media()
                    logging.info(
                        "telegram: Downloaded media file at : " + file)
                else:
                    discord_text = discord_text + \
                        "\nMedia attachment too large, maximum upload size with " \
                        "Level 3 boost allowed is 100 Mega Bytes."
            else:
                file = await event.download_media()
                logging.info(
                    "telegram: Downloaded media file at : " + file)

            if event.video or event.video_note:
                logging.info(
                    "telegram: found a video file called {}".format(file))
                logging.info("telegram: converting video to mp4 format")
                file2 = myutility.convert_to_mp4(file)
                os.remove(file)
                file = file2
                logging.info(
                    "telegram: conversion successfull, returned {}".format(file))

                # copy the media to webserver public directory if it follows these conditions
            if (media_size > media_min) and (config.small_uploads_only == False)\
                    and (config.large_upload_to_discord == False):
                url = server_copy(file)
                file = None
                discord_text = discord_text + \
                    "\nMedia attachment too large. Here's a direct link: " + url

        item = [discord_channels[telegram_channels.index(
            event.chat_id)], discord_text, file, media_size]
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
        update_str = "Reply to Old " + update_str
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
