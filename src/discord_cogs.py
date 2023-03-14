from discord.ext import commands
from config import logging
from telegram_end import load_channels
import config
import discord
import myutility
import telegram_end


class Channels(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_any_role(config.discord_admins))
    async def add(self, ctx: commands.Context, discord: str, *telegram):
        logging.info("discord: add() receieved telegram: {0}, discord {1}".format(
            telegram, discord))
        tg = list(telegram)
        for str in tg:
            if str[:4] != '-100':
                await ctx.send("discord: Error: telegram channel id should always start with `-` sign. " +
                               "Append `-100` to whatever channel id you have if you believe it is correct.")
                return

        myutility.add_channel(tg, discord)
        await ctx.send("discord: associated <#{}> with telegram id `{}` in memory.".format(discord, tg)
                       + "\nChanges are not final yet. When you're done `add`ing. Issue `save` command.")

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_any_role(config.discord_admins))
    async def begin(self, ctx: commands.Context):
        logging.info("discord: loading channels")
        myutility.load_channels()
        logging.info("discord: loaded channels")
        logging.info("discord: channels list: {}".format(config.channels))

        logging.info(
            "discord: Beginning update sequence in respective channels.")
        await ctx.send("discord: Beginning update sequence in respective channels.")
        for id in config.channels:
            logging.info("discord: begin: id: {}".format(int(id)))
            channel: discord.guild.GuildChannel = self.bot.get_channel(int(id))
            if channel:
                await channel.send("discord: Bot initiated. Watching for updates...")

        load_channels()
        logging.info("discord: channel loading sequence finished")

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_any_role(config.discord_admins))
    async def dump(self, ctx: commands.Context):
        await ctx.send("```json\n" + myutility.dump_channels() + "\n```")

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_any_role(config.discord_admins))
    async def toggle_direct_upload(self, ctx: commands.Context):
        if config.upload_to_discord:
            config.upload_to_discord = False
            await ctx.send("discord: direct uploads to discord disabled"
                           " for media larger than `7.9MB`.")
            logging.info("discord: disable direct uploads to discord for media"
                         " larger than 7.9 MB")
        else:
            config.upload_to_discord = True
            await ctx.send("discord: direct media uploads to discord enabled"
                           " for media size `x` where `7.9MB < x <= 50MB`")

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_any_role(config.discord_admins))
    async def ping(self, ctx: commands.Context):
        await ctx.send("discord: Ping acknowledged.\n"
                       "Hello, user <@{}>".format(ctx.message.author.id))
        logging.info("discord: Received a ping from user {} with id {}".format(
            ctx.message.author.name, ctx.message.author.id))

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_any_role(config.discord_admins))
    async def save(self, ctx: commands.Context):
        try:
            myutility.save_channels()
        except TypeError:
            await ctx.send("discord: Unable to save channels locally as JSON.")
        await ctx.send("discord: Saved channels locally as JSON.")

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_any_role(config.discord_admins))
    async def stop(self, ctx: commands.Context):
        config.channels.clear()
        telegram_end.discord_channels = []
        telegram_end.telegram_channels = []
        config.message_queue = config.asyncio.Queue(config.Qmaxsize)
        logging.info(
            "discord: stop: cleared channels dictionary. Updates stopped.")
        await ctx.send("discord: Updates have been stopped.\n"
                       "Restart updates by using the `u!begin` command or"
                       " Use `u!add` and `u!save` to start with a new set of channels"
                       " to fetch updates from")

    @add.error
    async def add_error(cog, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("`add` command used incorrectly.\n"
                           "Required arguments: `discord_id` `telegram_id`\n"
                           "Example: `u!add 1084119900014518000 -10017000021450`\n"
                           "`u!add 1084119907958018148 -10017594462431 -1001759446243`")
