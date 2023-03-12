import discord
import os

from config import logging, asyncio
from config import discord_token, LocalTelegramClient, log_handler
from config import message_queue, discord_channel_id
from telegram_end import telegram_main

async def process_queue(queue: asyncio.Queue, client: discord.Client):
  while True:
    logging.info("Starting to process queue now")

    item = await queue.get()

    logging.info("item received")
    logging.info("Sending item now")

    channel: discord.TextChannel = client.get_channel(discord_channel_id)

    # check necessary where multiple media files are sent from telegram
    if item[0] :
      await channel.send(item[0])
    if item[1] :
      with open(item[1], "rb") as media:
        await channel.send(file=discord.File(media, item[1]))
        os.remove(item[1])

    logging.info("item done")

    queue.task_done()

class LocalDiscordClientInstance(discord.Client):
  async def setup_hook(self):
    await LocalTelegramClient.start()
    self.loop.create_task(telegram_main())
    logging.info("discord: created telegram client instance")

  async def on_ready(self):
    logging.info("discord: logged in as {0}".format(self.user))
    self.loop.create_task(process_queue(message_queue, self))


def main():
  LocalDiscordClient = LocalDiscordClientInstance(intents=discord.Intents.default())
  LocalDiscordClient.run(discord_token, log_handler=log_handler)
  logging.info("discord_telegram: Logging out")

if __name__ == "__main__":
  main()