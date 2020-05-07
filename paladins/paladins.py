import aiohttp
import discord
import asyncio
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
        await ctx.send("Enter your paladins username")
        msg = await self.bot.wait_for("message", check=MessagePredicate.same_context(ctx))
        await ctx.send("Now enter your platform e.g pc, xbox, switch, ps4")
        msg1 = await self.bot.wait_for("message", check=MessagePredicate.same_context(ctx))
        player = msg.content
        platform = msg1.content
        async with self.session.get(f"https://nonsocial.herokuapp.com/api/lastmatch?query={player}&platform={platform}") as r:
            text = await r.text()
            text = text.split("|")
            text = text.replace("(", "").replace(")", "")
            await ctx.send(text)
            
    # shit rewrite
    @commands.command()
    async def champkda(self, ctx):
        await ctx.send("Enter your paladins username")
        msg = await self.bot.wait_for("message", check=MessagePredicate.same_context(ctx))
        await ctx.send("Now enter the champion you wish to see the stats of")
        msg1 = await self.bot.wait_for("message", check=MessagePredicate.same_context(ctx))
        await ctx.send("Now enter your platform e.g pc, switch, xbox, ps4")
        msg2 = await self.bot.wait_for("message", check=MessagePredicate.same_context(ctx))
        player = msg.content
        platform = msg2.content
        champion = msg1.content
        async with self.session.get(f"https://nonsocial.herokuapp.com/api/kda?player={player}&champion={champion}&platform={platform}") as r:
            text = await r.text()
            text = text.split('|')
            await ctx.send(text)