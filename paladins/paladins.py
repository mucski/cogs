import aiohttp
import discord
from redbot.core import commands, Config
from redbot.core.utils.predicates import MessagePredicate

class Paladins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #thanks DevilXD
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        asyncio.create_task(self.session.close())
          
    # shit rewrite
    @commands.command()
    async def last(self, ctx):
        msg1 = await ctx.send("Enter your paladins username")
        await bot.wait_for("msg1", check=MessagePredicate.same_context(ctx))
        msg2 = await ctx.send("Now enter your platform e.g pc, xbox, switch, ps4")
        await bot.wait_for("msg2", check=MessagePredicate.same_context(ctx))
        player = msg1.content
        platform = msg2.content
        async with self.session.get(f"https://nonsocial.herokuapp.com/api/lastmatch?query={player}&platform={platform}") as r:
            text = await r.text()
            text = text.split('|')
            await ctx.send(text)