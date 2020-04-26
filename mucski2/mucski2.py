import asyncio
import discord
import datetime
import itertools
import math
import random
import time
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
    async def hello(self, ctx, channel: discord.TextChannel=None):
        msg = await ctx.send("Input bellow what you want to say in another channel")
        pred = MessagePredicate.same_context(ctx)
        try:
            msg = await self.bot.wait_for('message', timeout=30, check=pred)
        except asyncio.TimeoutError:
            return await ctx.send("Timedout")
        await channel.send(msg.content)
        start_adding_reactions(msg.content, ReactionPredicate.self.emoji)
        await ctx.send("Successfully sent your message")
        
    @commands.command()
    async def game(self, ctx):
        msg = await ctx.send("Use the controls bellow to pick the lock. ")
        for emoji in emojis:
            await msg.add_reaction(emoji)
        pred = ReactionPredicate.with_emojis(emoji, message=msg, user=ctx.author)
        try:
            await self.bot.wait_for('reaction_add', timeout=60, check=pred)
        except asyncio.TimeoutError:
            return await ctx.send("Timed out. ")
            return msg.clear_reactions()
        emoji = emojis[pred.result]
        if emoji == '❌': 
            await msg.clear_reactions()
            return await msg.edit(content="okay shutting down")
        elif emoji == '◀️':
            dir = '<'
        elif emoji == '▶️':
            dir = '>'
        await msg.remove_reaction(emoji, ctx.author)
        await msg.edit(dir)
    
    @commands.command()
    async def who(self, ctx, channel: discord.TextChannel, messageid: int):
        try:
            msg = await channel.fetch_message(messageid)
        except HTTPException:
            return await ctx.send("couldn't find that message")
        reaction = discord.utils.get(msg.reactions, emoji=self.emoji)
        if reaction is None:
            return await ctx.send("There were no reactions. ")
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