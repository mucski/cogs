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
        self.loc = {
            "sewer": "You descended into the sewers hoping to find a dancing clown, found {cookie} cookies instead. ",
            "dog": "Found {cookie} cookies in dog.... Shit. Why would you do that.. ",
            "toilet": "As disgusting as it sounds, you found {cookie} cookies in the toilet bowl. Lucky no one used the toilet before you. ", 
            "box": "You rummaged through a box of forgotten items, found {cookie} cookies. Lucky you. ", 
            "drawer": "After going through many panties, a dildo, and a hand gun, you found {cookie} cookies wrapped in socks", 
            "forest": "You were looking for Little Red Riding Hood, instead you found {cookie} cookies hidden in a tree bark. ", 
            "set": "You are the next star for Ironing Man. While equipping his armor you found {cookie} cookies in one of the hidden compartments. "
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
        r = random.sample(list(self.loc.keys()), 3)
        await ctx.send("Chose a location to search from bellow")
        await ctx.send(f"``{r[0]}``, ``{r[1]}``, ``{r[2]}``")
        def check(m):
            return m.content == r[0] or m.content == r[1] or m.content == r[2] and m.channel == ctx.channel and m.author == ctx.author
        try:
            msg = await ctx.bot.wait_for('message', timeout=10, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("Timed out.")
        if msg.content == r[0]:
            return await ctx.send(f"{self.loc[r[0]]}")
        elif msg.content == r[1]:
            return await ctx.send(f"{self.loc[r[1]]}")
        elif msg.content == r[2]:
            return await ctx.send(f"{self.loc[r[2]]}")
    