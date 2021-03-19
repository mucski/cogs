import arez
# from PIL import ImageOps, ImageDraw, Image, ImageFont
from redbot.core import commands
import asyncio
# import aiohttp
# from io import BytesIO
import humanize
from datetime import datetime
import discord


class Paladins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.f = open("/home/ubuntu/key.txt", "r")
        self.auth = self.f.readline()
        self.devid = self.f.readline()
        self.api = arez.PaladinsAPI(dev_id=self.devid.strip(),
                                    auth_key=self.auth.strip())

    def cog_unload(self):
        asyncio.createTask(self.api.close())
        self.f.close()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            exc = error.original
            if isinstance(exc, arez.Unavailable):
                await ctx.send("HiRez API is offline or unavaiable.")
                return
            if isinstance(exc, arez.Private):
                await ctx.send("Requested profile is set to private")
                return
            if isinstance(exc, arez.NotFound):
                await ctx.send("Player was not found")
                return
        await ctx.bot.on_command_error(ctx, error, unhandled_by_cog=True)

    async def get_champ_image(self, champ):
        champ = champ.lower()
        if "bomb" in champ:
            champ = "bomb-king"
        if "sha" in champ:
            champ = "sha-lin"
        if "mal" in champ:
            champ = "maldamba"
        url = "https://web2.hirez.com/paladins/champion-icons/" \
            + str(champ) + ".jpg"
        return url

    @commands.command()
    async def hitest(self, ctx, champ):
        res = await self.get_champ_image(champ)
        await ctx.send(res)

    @commands.command()
    async def stats(self, ctx, player, platform="PC"):
        platform = arez.Platform(platform)
        if player.isdecimal():
            player = await self.api.get_player(player)
        else:
            player_obj = await self.api.search_players(player, platform)
            player = await player_obj[0]
        desc = (
            "**__Player Stats__**\n"
            f"```Account level: {player.level}\n"
            f"Playtime: {int(player.playtime.total_hours())} hours\n"
            f"Region: {player.region}\n"
            f"Champions Owned: {player.champion_count}\n"
            f"Achievements Unlocked: {player.total_achievements}\n"
            f"Account Created: "
            f"{humanize.naturaltime(datetime.utcnow() - player.created_at)}\n"
            f"Last Login: "
            f"{humanize.naturaltime(datetime.utcnow() - player.last_login)}\n"
            "```\n\n"
            f"**__Casual Stats__**\n"
            f"```Win Rate: "
            f"{player.casual.wins}/{player.casual.losses}"
            f"({player.casual.winrate_text})\n"
            f"Deserted: {player.casual.leaves}\n```"
            "\n\n"
            f"**__Ranked Stats Season {player.ranked_best.season}__**\n"
            f"```Win Rate: "
            f"{player.ranked_best.wins}/{player.ranked_best.losses}"
            f"({player.ranked_best.winrate_text})\n"
            f"Deserted: {player.ranked_best.leaves}\n"
            f"Ranked Type: {player.ranked_best.type}\n"
            f"Current Rank: {player.ranked_best.rank}"
            f" ({player.ranked_best.points} TP)\n```"
        )
        e = discord.Embed(color=await self.bot.get_embed_color(ctx),
                          title=f"{player.name}({player.platform})"
                                f"_({player.title})_")
        e.description = desc
        e.set_thumbnail(url=player.avatar_url)
        e.set_footer(text=f"Player ID: {player.id}")
        await ctx.send(embed=e)
