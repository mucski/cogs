from redbot.core import commands, Config
import random
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import ReactionPredicate
import discord
import asyncio


class Test(commands.Cog):
    def __init__(self, bot):
        self.conf = Config.get_conf(self, 9340293423)
        defaults = {
            "msgs": {}
        }
        self.conf.register_guild(**defaults)
        self.bot = bot

    @commands.command()
    async def msglaunch(self, ctx):
        msg = await self.conf.guild(ctx.guild).msgs()
        await ctx.send(msg)

    @commands.command()
    async def msgdefine(self, ctx):
        msg1 = "Title"
        msg2 = "Content"
        msg = await self.conf.guild(ctx.guild).msgs()
        msg += await self.conf.guild(ctx.guild).set_raw.msgs({msg1: msg2})
        await ctx.send("Done")