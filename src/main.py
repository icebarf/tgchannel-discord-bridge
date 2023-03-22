# main.py - the actual bridge program's main file.
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

import discord
from discord.ext import commands
import os

import discord_cogs

from config import logging, asyncio
from config import discord_token, log_handler
import config
from telegram_end import telegram_main
import telegram_end

BoostLevel2: int = 7
BoostLevel3: int = 14


async def process_queue(queue: asyncio.Queue, client: discord.Client) -> None:
    while True:
        logging.info("discord: Starting to process queue now")

        item = await queue.get()

        logging.info("discord: item received")
        logging.info("discord: Sending item now")

        discord_channel: discord.TextChannel = client.get_channel(item[0])
        discord_title: str = item[1]
        discord_text: str = item[2]
        is_attachment_video = item[3]
        discord_attachment: str = item[4]
        discord_attachment_size: int = item[5]
        direct_url: str = item[6]
        boost_cnt: int = discord_channel.guild.premium_subscription_count

        # check necessary where multiple media files are sent from telegram
        embed = discord.Embed(title=discord_title, colour=0x03b1fc)

        if discord_text:
            embed.description = discord_text
            logging.info("discord: embed_description: %s", embed.description)
            # await discord_channel.send(discord_text)

        discord_file: discord.File = None
        if discord_attachment:
            logging.info("discord: attachment: name: %s", discord_attachment)
            logging.info(
                "discord: attachment: is_attachment_video: %s", is_attachment_video)
            logging.info("discord: attachment: attachment_size: %s",
                         discord_attachment_size)
            if (boost_cnt >= BoostLevel3) and (discord_attachment_size <= telegram_end.media_max):
                discord_file = discord.File(
                    discord_attachment, filename=discord_attachment)
                logging.info("discord: reached boost level 3 part")
                if not is_attachment_video:
                    logging.info("discord: setting image url in embed")
                    if not discord_text:
                        embed.description = "With previous update:"
                    embed.set_image(url="attachment://"+discord_attachment)
            elif (boost_cnt >= BoostLevel2 and boost_cnt < BoostLevel3) and (discord_attachment_size <= (telegram_end.media_max / 2)):
                discord_file = discord.File(
                    discord_attachment, filename=discord_attachment)
                logging.info("discord: reached boost level 2 part")
                if not is_attachment_video:
                    logging.info("discord: setting image url in embed")
                    if not discord_text:
                        embed.description = "With previous update:"
                    embed.set_image(url="attachment://"+discord_attachment)
            elif (discord_attachment_size <= telegram_end.media_min):
                discord_file = discord.File(
                    discord_attachment, filename=discord_attachment)
                logging.info("discord: reached default part")
                if not is_attachment_video:
                    logging.info("discord: setting image url in embed")
                    if not discord_text:
                        embed.description = "With previous update:"
                    embed.set_image(url="attachment://"+discord_attachment)
            else:
                embed.description = embed.description + \
                    "\nMedia too large for non boosted server."

        await discord_channel.send(file=discord_file, embed=embed)

        if direct_url:
            await discord_channel.send(direct_url)

        if discord_attachment:
            os.remove(discord_attachment)

        logging.info("discord: item done")
        queue.task_done()


class LocalDiscordClientInstance(commands.Bot):
    async def setup_hook(self) -> None:
        await config.LocalTelegramClient.start()
        self.loop.create_task(telegram_main())
        logging.info("discord: created telegram client instance")
        await LocalDiscordClientInstance.add_cog(self, discord_cogs.Channels(self))
        logging.info("discord: loaded cogs")

    async def on_ready(self) -> None:
        logging.info("discord: logged in as {0}".format(self.user))
        self.loop.create_task(process_queue(config.message_queue, self))


def main():
    LocalDiscordClient = LocalDiscordClientInstance(
        command_prefix="u!", intents=discord.Intents.all())
    LocalDiscordClient.run(discord_token, log_handler=log_handler)
    logging.info("discord_telegram: Logging out")


if __name__ == "__main__":
    main()
