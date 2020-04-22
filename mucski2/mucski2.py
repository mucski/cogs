import asyncio
import discord
import datetime
import itertools
import math
import random
import time 

from redbot.core import bank, checks, commands, Config
from redbot.core.utils.chat_formatting import bold, box, humanize_list, humanize_number, pagify
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS 
from redbot.core.utils import predicates

class Mucski2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def hello(self, ctx):
        msg = await ctx.send("Hi, what do you want?!")
        try:
            check = MessagePredicate.same_context(ctx)
            msg = await ctx.bot.wait_for("message", check=check, timeout=60)
        except asyncio.TimeoutError:
            #time expired end command
            return
        edited = check.result
        await msg.edit(content=edited)
        
        