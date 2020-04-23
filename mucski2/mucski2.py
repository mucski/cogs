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
        loc = {
            "sewer": "You went to look for cookies in the sewer.",
            "dog": "I am not sure how you gonna search a dog for cookies but i won't judge",
            "toilet": "You must be joking right now..."
        }
        
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
    async def ugay(self, ctx):
        await ctx.send("Say, I'm gay!")
        def check(m):
            return m.content == "I'm gay!" or m.content == "No u" and m.channel == ctx.channel
        try:    
            msg = await ctx.bot.wait_for('message', timeout=60, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("You can't even do what I ask of you properly")
        if msg.content == "I'm gay!":
            await ctx.send(f"Congrats {msg.author.mention} you're now gay. ")
        else:
            return await ctx.send("No, your mom!")
        
    @commands.command()
    async def who(self, ctx, channel: discord.TextChannel, messageid: int):
        if messageid is None:
            return await ctx.send("Invalid channel id")
        reaction = discord.utils.get(messageid.reactions, emoji='❤️')
        if reaction is None:
            return await channel.send("There were no reactions. ")
        async for users in reaction.users():
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
        rand_loc = random.choice(list(loc.key()))
        await ctx.send("Chose a location to search from bellow")
        await ctx.send(f"{rand_loc}")
        def check(m):
            return m.content == {rand_loc} and m.channel == ctx.channel and m.author == ctx.author
        try:
            msg = await ctx.bot.wait_for('message', timeout=60, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("Timed out.")
        if msg.content == rand_loc:
            return await ctx.send(f"{loc[rand_loc]}")
    