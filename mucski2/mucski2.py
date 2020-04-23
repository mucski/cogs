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
from redbot.core.utils.predicates import MessagePredicate

class Mucski2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, 282828485)
        
    @commands.command()
    async def hello(self, ctx):
        msg = await ctx.send("Hi, what do you want?!")
        predicate = MessagePredicate.same_context(ctx)
        try:        
            m = await ctx.bot.wait_for('message', timeout=60, check=predicate)
        except asyncio.TimeoutError:
            return
        poop = f"you said {m.content}"
        await msg.edit(content=poop)
        await msg.add_reaction('\U0001F39F')
        await msg.add_reaction('❤️')
        return
    
    @commands.command()
    async def gw(self, ctx, messageid: int, *, msg):
        if msg is None:
            await ctx.send('error')
        else:
            messageid = await channel.fetch_message(messageid)
            await ctx.send(msg)
            await asyncio.sleep(2)
            await msg.add_reaction('❤️')
        
    @commands.command()
    async def who(self, ctx, channel: discord.TextChannel, messageid: int):
        msg = await channel.fetch_message(messageid)
        if messageid is None:
            return await ctx.send("Invalid channel id")
        reaction = discord.utils.get(msg.reactions, emoji='❤️')
        if reaction is None:
            return await channel.send("no one")
        for users in reaction.users():
            member = ctx.guild.get_member(user.id)
            if member:
                users.append(user)
        await ctx.send(users)
        
    @commands.command()
    async def oof(self, ctx):
        msg = "https://media2.giphy.com/media/S3Qafn57JDnsfRfbFc/giphy.gif"
        e = discord.Embed()
        e.set_image(url=msg)
        await ctx.send(embed=e)
        
    @commands.command()
    async def search(self, ctx):
        pass
    
    