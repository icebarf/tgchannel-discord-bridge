import myutility, discord
from config import logging
from discord.ext import commands

class Channels(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @commands.command()
  async def add(self, ctx: discord.TextChannel, discord: str, telegram: str):
    logging.info("discord: add() receieved telegram: {0}, discord {1}".format(telegram, discord))

    if telegram[:4] != '-100':
      await ctx.send("discord: Error: telegram channel id should always start with `-` sign. " +
               "Append `-100` to whatever channel id you have if you believe it is correct.")
      return

    myutility.add_channel(telegram, discord)
    await ctx.send("discord: associated <#{}> with telegram id `{}` in memory.".format(discord, telegram))

  @commands.command()
  async def save(self, ctx: discord.TextChannel):
    logging.info("discord: We're inside the save command now")
    try:
      myutility.save_channels()
    except TypeError:
      await ctx.send("discord: Unable to save channels locally as JSON.")
    await ctx.send("discord: Saved channels locally as JSON.")

  @add.error
  async def add_error(cog, ctx: discord.TextChannel, error):
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send("`add` command used incorrectly.\n"
                     "Required arguments: `discord_id` `telegram_id`\n"
                     "Example: `u!add 1084119900014518000 -10017000021450`")

async def setup(bot: commands.Bot) -> None:
    bot.add_cog(Channels(bot))