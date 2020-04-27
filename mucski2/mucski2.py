import asyncio
import discord
import datetime
import itertools
import math
import random
import time
import re
from discord.ext import tasks, commands

from redbot.core import bank, checks, commands, Config
from redbot.core.utils.chat_formatting import bold, box, humanize_list, humanize_number, pagify
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core.utils.predicates import MessagePredicate
from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions

emojis = ('◀️','▶️','❌')

class Mucski2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, 282828485)
        defaults = {
            "gold": 0,
            "datetime": []
        }
    
    def gettime(self):
        for message in channel.history(limit=5):
            delta = datetime.datetime.utcnow() - message.created_at
        return delta
    
    @commands.command()
    async def emote(self, ctx, emoji: discord.PartialEmoji):
        e = discord.Embed()
        e.set_image(url=emoji.url)
        await ctx.send(embed=e)
    
    @commands.command()
    async def who(self, ctx, channel: discord.TextChannel, messageid: int):
        try:
            msg = await channel.fetch_message(messageid)
        except HTTPException:
            return await ctx.send("couldn't find that message")
        #users = await msg.reactions[0].users().flatten()
        users = []
        async for user in msg.reactions[0].users():
            users.append(user)
        randomized = random.choice(users)
        await ctx.send(randomized.name)
        
    @commands.command()
    async def oof(self, ctx):
        msg = "https://media2.giphy.com/media/S3Qafn57JDnsfRfbFc/giphy.gif"
        e = discord.Embed()
        e.set_image(url=msg)
        await ctx.send(embed=e)
        
    @commands.command()
    async def avatar(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        e = discord.Embed()
        e.set_image(url=member.avatar_url)
        await ctx.send(embed=e)
    
        
    @commands.command()
    async def emtest(self, ctx):
        e = discord.Embed(description="Profile ")
        e.set_thumbnail(url=ctx.author.avatar_url)
        e.add_field(name="Cookies in your jar {cookies}", value="dsdg")
        e.add_field(name="Daily claimed: Yes", value="dddg")
        e.add_field(name="Items owned: 0", value="ddfh")
        e.add_field(name="Daily cooldown: 0s", value="dddfh")
        e.add_field(name="Locks picked: 0", value="fdssh")
        e.add_field(name="Field ready to farm: No", value="sssfhh")
        e.set_image(url="https://comicvine1.cbsistatic.com/uploads/scale_medium/11125/111253436/6733777-4.jpg")
        e.set_footer(text="Powered by your mom")
        await ctx.send(embed=e)
        
    @commands.command()
    async def startevent(self, ctx):
        gettime = async gettime()
        msg="this is a test done on {}".format(gettime)
        await ctx.send(msg)
        