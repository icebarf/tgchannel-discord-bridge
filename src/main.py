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
        discord_text: str = item[1]
        discord_attachment: str = item[2]
        discord_attachment_size: int = item[3]
        boost_cnt: int = discord_channel.guild.premium_subscription_count
        # check necessary where multiple media files are sent from telegram
        if discord_text:
            await discord_channel.send(discord_text)
        if discord_attachment:
            with open(discord_attachment, "rb") as media:
                if (boost_cnt >= BoostLevel3) and (discord_attachment_size <= telegram_end.media_max):
                    await discord_channel.send(file=discord.File(media, discord_attachment))
                elif (boost_cnt >= BoostLevel2 and boost_cnt < BoostLevel3) and (discord_attachment_size <= (telegram_end.media_max / 2)):
                    await discord_channel.send(file=discord.File(media, discord_attachment))
                elif (discord_attachment_size <= telegram_end.media_min):
                    await discord_channel.send(file=discord.File(media, discord_attachment))
                else:
                    await discord_channel.send("Media too large for non boosted server.")
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
