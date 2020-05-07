import aiohttp
import discord
from redbot.core import commands, Config

class Paladins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #thanks DevilXD
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        asyncio.create_task(self.session.close())
          
    # shit rewrite
    @commands.command()
    async def last(self, ctx, *, player, platform="pc"):
        async with self.session.get(f"https://nonsocial.herokuapp.com/api/lastmatch?query={player}&platform={platform}") as r:
        text = await r.text()
        text = text.split('|')
        await ctx.send(text)