# discord_cogs.py - functions defining the discord bot's interface
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

from discord.ext import commands
from config import logging
from telegram_end import load_channels
import config
import myutility
import telegram_end


class Channels(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_any_role(config.data.discord_admins))
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
    @commands.check_any(commands.is_owner(), commands.has_any_role(config.data.discord_admins))
    async def begin(self, ctx: commands.Context):
        logging.info("discord: loading channels")
        myutility.load_channels()
        logging.info("discord: loaded channels")
        logging.info("discord: channels list: {}".format(config.channels))

        logging.info(
            "discord: Beginning update sequence in respective channels.")
        await ctx.send("discord: Beginning update sequence in respective channels.")
        update: str = "Channels to send updates in: "
        for id in config.channels:
            logging.info("discord: begin: id: {}".format(int(id)))
            update = update + "<#" + str(id) + "> "
        await ctx.send(update)
        logging.info(update)

        load_channels()
        logging.info("discord: channel loading sequence finished")

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_any_role(config.data.discord_admins))
    async def dump(self, ctx: commands.Context):
        await ctx.send("```json\n" + myutility.dump_channels() + "\n```")

    @commands.command()
    async def send_help(self, ctx: commands.Context):
        await ctx.send("<https://github.com/icebarf/tgchannel-discord-bridge#discord-commands>"
                       "\n<https://github.com/icebarf/tgchannel-discord-bridge#use-examples-in-a-discord-server>")

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_any_role(config.data.discord_admins))
    async def ping(self, ctx: commands.Context):
        await ctx.send("discord: Ping acknowledged.\n"
                       "Hello, user <@{}>".format(ctx.message.author.id))
        logging.info("discord: Received a ping from user {} with id {}".format(
            ctx.message.author.name, ctx.message.author.id))

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_any_role(config.data.discord_admins))
    async def save(self, ctx: commands.Context):
        try:
            myutility.save_channels()
        except TypeError:
            await ctx.send("discord: Unable to save channels locally as JSON.")
        await ctx.send("discord: Saved channels locally as JSON.")

    @commands.command()
    async def source(self, ctx: commands.Context):
        await ctx.send("https://github.com/icebarf/tgchannel-discord-bridge")

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_any_role(config.data.discord_admins))
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

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_any_role(config.data.discord_admins))
    async def toggle_small_uploads(self, ctx: commands.Context):
        config.small_uploads_only = not config.small_uploads_only
        if config.small_uploads_only:
            await ctx.send("discord: Enabled: Small media upload.\n"
                           "Media only smaller than or equal to {} Mega Bytes is allowed".format(
                               (telegram_end.media_min / 1024) / 1024))
            logging.info("discord: Enabled: Small media upload.\n"
                         "Media only smaller than or equal to {} Mega Bytes is allowed".format(
                             (telegram_end.media_min / 1024) / 1024))
        else:
            await ctx.send("discord: Disabled: Small media uploads.\n"
                           "Media larger than {} Mega Bytes is allowed. Depending on your configuraiton"
                           " the media will be directly uploaded to discord or saved at the public directory of webserver".format(
                               (telegram_end.media_min / 1024) / 1024))
            logging.info("discord: Disabled: Small media uploads.\n"
                         "Media larger than {} Mega Bytes is allowed. Depending on your configuraiton"
                         " the media will be directly uploaded to discord or saved at the public directory of webserver".format(
                             (telegram_end.media_min / 1024) / 1024))

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_any_role(config.data.discord_admins))
    async def toggle_direct_large_uploads(self, ctx: commands.Context):
        config.large_upload_to_discord = not config.large_upload_to_discord
        if config.large_upload_to_discord:
            config.small_uploads_only = False
            await ctx.send("discord: Enabled: direct media uploads to discord"
                           " for media size `x` where `7.9MB < x <= 100MB`")
            logging.info("discord: Enabled: direct media uploads to discord"
                         " larger than 7.9 MB")
        else:
            await ctx.send("discord: Disabled: direct media uploads to discord"
                           " for media size `x` where `7.9MB < x <= 100MB`")
            logging.info("discord: Disabled: direct media uploads to discord"
                         " larger than 7.9 MB")

    @add.error
    async def add_error(cog, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("`add` command used incorrectly.\n"
                           "Required arguments: `discord_id` `telegram_id`\n"
                           "Example: `u!add 1084119900014518000 -10017000021450`\n"
                           "`u!add 1084119907958018148 -10017594462431 -1001759446243`")
