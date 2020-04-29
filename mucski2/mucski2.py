import asyncio
import discord
import itertools
import math
import random
import time
import re
import calendar
from discord.ext import tasks, commands
from datetime import datetime, timedelta

from redbot.core import bank, checks, commands, Config
from redbot.core.utils.chat_formatting import bold, box, humanize_list, humanize_number, pagify, humanize_timedelta
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
            "datetime": "",
            "daily_stamp": 0,
            "daily_timer": 0,
        }
        self.conf.register_user(**defaults)
    
    #Get thet bot color for embeds 'await self.color(ctx)'
    async def color(self, ctx):
        return await ctx.bot.get_embed_color(location=ctx.channel)
    
    @commands.command(name="emote", aliases=['emoji'])
    async def emote(self, ctx, emoji: discord.PartialEmoji):
        await ctx.send(emoji.url)
    
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
        e = discord.Embed(color=await self.color(ctx))
        e.set_image(url=msg)
        await ctx.send(embed=e)
        
    @commands.command(name="avatar", aliases=['pfp'])
    async def avatar(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        await ctx.send(member.avatar_url)
        
    @commands.command()
    async def setcd(self, ctx, amt: int):
        #try with minutes first until better solution
        member = ctx.author
        timer = timedelta(minutes=amt)
        now = datetime.utcnow().replace(microsecond=0)
        future = now + timer
        await self.conf.user(member).daily_stamp.set(future.timestamp())
        await self.conf.user(member).daily_timer.set(amt)
        await ctx.send(f"successfully set {future}")
        
    @commands.command()
    async def resetcd(self, ctx):
        await self.conf.user(ctx.author).daily_stamp.clear()
        await ctx.send("Done")
        
    @commands.command()
    async def test(self, ctx):
        member = ctx.author
        daily_stamp = await self.conf.user(member).daily_stamp()
        #convert stamp to time
        now = datetime.utcnow().replace(microsecond=0)
        if now.timestamp() < daily_stamp:
            await ctx.send(f"command on cooldown until {datetime.fromtimestamp(daily_stamp)}")
        else:
            await ctx.send("yay it works")
            await self.conf.user(member).daily_timer()
            timer = timestamp(minutes=daily_timer)
            next_cd = now + timer
            await self.conf.user(member).daily_stamp.set(next_cd.timestamp())

    @commands.command()
    async def rol(self, ctx):
        him = random.randint(1,6)
        you = random.randint(1,6)
        if you < 6 and him > you:
            msg = "Oops, dealer won."
        elif you == him:
            msg = "Looks like its a tie."
        elif him < 6 and you > him:
            msg = "Yay you won."
        description = (
            f'You rolled: - **{you}**\n'
            f'Dealer rolled: - **{him}**\n\n'
            f'{msg}'
        )
        e = discord.Embed(color = await self.color(ctx), description=description)
        e.set_thumbnail(url=ctx.bot.user.avatar_url)
        e.set_author(name=f"{ctx.author}'s dice roll game.", icon_url=f"{ctx.author.avatar_url}")
        e.set_footer(text=datetime.datetime.utcnow())
        await ctx.send(embed=e)
        