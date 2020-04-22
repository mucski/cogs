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

class Mucski2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def hello(self, ctx):
        msg = await ctx.send("Hi, what do you want?!")
        pass
        
    @commands.command()
    async def oof(self, ctx):
        msg = "https://media2.giphy.com/media/S3Qafn57JDnsfRfbFc/giphy.gif"
        e = discord.Embed()
        e.set_image(url=msg)
        await ctx.send(embed=e)