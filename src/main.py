import discord
from discord.ext import commands
import os

import myutility
import discord_cogs

from config import logging, asyncio
from config import discord_token, LocalTelegramClient, log_handler
from config import message_queue, discord_channel_id
from telegram_end import telegram_main

async def process_queue(queue: asyncio.Queue, client: discord.Client) -> None:
  while True:
    logging.info("discord: Starting to process queue now")

    item = await queue.get()

    logging.info("discord: item received")
    logging.info("discord: Sending item now")

    channel: discord.TextChannel = client.get_channel(discord_channel_id)

    # check necessary where multiple media files are sent from telegram
    if item[0] :
      await channel.send(item[0])
    if item[1] :
      with open(item[1], "rb") as media:
        await channel.send(file=discord.File(media, item[1]))
        os.remove(item[1])

    logging.info("discord: item done")
    queue.task_done()

class LocalDiscordClientInstance(commands.Bot):
  async def setup_hook(self) -> None:
    await LocalTelegramClient.start()
    self.loop.create_task(telegram_main())
    logging.info("discord: created telegram client instance")
    await LocalDiscordClientInstance.add_cog(self, discord_cogs.Channels(LocalDiscordClientInstance))
    logging.info("discord: loaded cogs")

  async def on_ready(self) -> None:
    logging.info("discord: logged in as {0}".format(self.user))
    self.loop.create_task(process_queue(message_queue, self))

def main():
  LocalDiscordClient = LocalDiscordClientInstance( command_prefix="u!", intents=discord.Intents.all())
  LocalDiscordClient.run(discord_token, log_handler=log_handler)
  logging.info("discord_telegram: Logging out")

if __name__ == "__main__":
  main()