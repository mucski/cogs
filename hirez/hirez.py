import arez
from redbot.core import checks, commands
import asyncio
import humanize
from datetime import datetime
import discord
from redbot.core.utils.chat_formatting import pagify, text_to_file
import aiohttp
import aiofiles
import json
import math
from tabulate import tabulate
from collections import Counter


class HiRez(commands.Cog):
    """Paladins stats cog by Mucski
    For a better experience you should link yout discord account to hirez
    that way you can use most commands without typing anything else but the command itself

    example: [p]champstats
    """
    def __init__(self, bot):
        self.bot = bot
        self.f = open("/root/mucski/stuff/key.txt", "r")
        self.auth = self.f.readline()
        self.devid = self.f.readline()
        self.api = arez.PaladinsAPI(dev_id=self.devid.strip(), auth_key=self.auth.strip())

    def cog_unload(self):
        asyncio.createTask(self.api.close())
        self.f.close()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            exc = error.original
            if isinstance(exc, arez.Unavailable):
                await ctx.send("```\nHiRez API is unavailable.\n```")
                return
            if isinstance(exc, arez.Private):
                await ctx.send("```\nRequested profile is set to private\n```")
                return
            if isinstance(exc, arez.NotFound):
                await ctx.send("```\nNot found!\n```")
                return
            if isinstance(exc, aiohttp.ClientResponseError):
                await ctx.send("```\nTimed out. Try again in a minute\n```")
            if isinstance(exc, arez.exceptions.HTTPException):
                await ctx.send("```\nSomething went wrong, try again with another user/id/name or try agian later\n```")
        await ctx.bot.on_command_error(ctx, error, unhandled_by_cog=True)

    @commands.command()
    async def status(self, ctx):
        """Paladins server statuses
        Green means online, red means offline, yellow means limited access
        """
        status = await self.api.get_server_status()
        stringus = ""
        for k, v in status.statuses.items():
            if v.status == "Operational":
                server = "🟢"
            elif v.status == "Limited Access":
                server = "🟡"
            else:
                server = "🔴"
            desc = (
                "```\n"
                f"Platform: {v.platform}\n"
                f"Status: {server} {v.status}\n"
                f"Version: {v.version}\n\n"
                "```"
            )
            stringus += desc
        e = discord.Embed(title="Paladins Server Status", color=await self.bot.get_embed_color(ctx), description=stringus)
        e.set_footer(text=f"Current time: {status.timestamp.strftime('%c')}")
        await ctx.send(embed=e)

    @commands.command()
    @checks.is_owner()
    async def downloadchamps(self, ctx):
        """
        This downloads all the champion avatars into the folder specified bellow
        """
        entry = await self.api.get_champion_info()
        for champ in entry.champions:
            async with aiohttp.ClientSession() as session:
                url = champ.icon_url
                name = champ.name.lower().replace(" ","-").replace("'","")
                async with session.get(url) as resp:
                    if resp.status == 200:
                        f = await aiofiles.open(f'root/mucski/stuff/icons/avatars/{name}.jpg', mode='wb')
                        await f.write(await resp.read())
                        await f.close()
        await ctx.tick()

    @commands.command()
    async def stats(self, ctx, name=None, platform="PC"):
        """Returns a players stats.
        [p]stats none or [p]stats (player) (platform)
        """
        if name is None:
            # use the ID of the caller
            discord_id = ctx.author.id
            try:
                player = await self.api.get_from_platform(discord_id, arez.Platform.Discord)
                player = await player
            except arez.NotFound:
                await ctx.send("```\nDiscord account not linked to HiRez. Please link it first\n```")
                return
        else:
            # player is a str here
            player_list = await self.api.search_players(name, arez.Platform(platform))
            player = await player_list[0]
        status = await player.get_status()
        if status.status == 5 or status.status == 0:
            player_status = "Last login: {}".format(humanize.naturaltime(datetime.utcnow() - player.last_login))
        else:
            player_status = "Currently: {}".format(status.status)
        desc = (
            "**__Player Stats__**\n"
            f"```\nAccount level: {player.level}\n"
            f"Playtime: {math.floor(player.playtime.total_hours())} hours\n"
            f"Region: {player.region}\n"
            f"Champions Owned: {player.champion_count}\n"
            f"Achievements Unlocked: {player.total_achievements}\n"
            "Account Created: "
            f"{humanize.naturaltime(datetime.utcnow() - player.created_at)}\n"
            f"{player_status}"
            "\n```"
            "**__Casual Stats__**\n"
            "```\nWin Rate: "
            f"{player.casual.wins}/{player.casual.losses}"
            f" ({player.casual.winrate_text})\n"
            f"Deserted: {player.casual.leaves}\n```"
            f"**__Ranked Stats Season {player.ranked_best.season}__**\n"
            f"```\nWin Rate: "
            f"{player.ranked_best.wins}/{player.ranked_best.losses}"
            f" ({player.ranked_best.winrate_text})\n"
            f"Deserted: {player.ranked_best.leaves}\n"
            f"Ranked Type: {player.ranked_best.type}\n"
            f"Current Rank: {player.ranked_best.rank}"
            f" ({player.ranked_best.points} TP)\n```"
        )
        if status.status == 5 or status.status == 0:
            status_emoji = "🔴"
        else:
            status_emoji = "🟢"
        e = discord.Embed(color=await self.bot.get_embed_color(ctx),
                          title=f"{status_emoji} {player.name} ({player.platform}) "
                                f"_({player.title})_")
        e.description = desc
        e.set_thumbnail(url=player.avatar_url)
        e.set_footer(text=f"Player ID: {player.id}")
        await ctx.send(embed=e)
