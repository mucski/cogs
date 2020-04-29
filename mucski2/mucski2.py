import asyncio
import discord
import itertools
import math
import random
import time
import re
import calendar
from discord.ext import tasks, commands
from datetime import datetime

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
            "datetime": "",
            "daily_stamp": 0,
        }
        self.conf.register_user(**defaults)
        
    async def get_time(self, member):
        return await self.conf.user(member).datetime()
    
    async def set_time(self, member, time):
        return await self.conf.user(member).datetime.set(time)
    
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
    async def test(self, ctx):
        member = ctx.author
        timer = await self.conf.user(member).daily_cd()
        timer = self.time_converter(timer)
        now = calendar.timegm(datetime.utcnow().utctimetuple())
        now = await self.set_time(member,now)
        now2 = await self.get_time(member)
        if timer - now2 != now:
            cock = timer - now2
            cock = datetime.fromtimestamp(cock)
            date_format = "%d/%m %H:%M"
            cock = cock.strftime(date_format)
            await ctx.send(f"on cooldown until {cock}")
            
    @commands.command()
    async def timeop(self, ctx):
        #date_format = "%d/%m/%Y %H%M%S" #Used for a and b
        date_format = "%d/%m %H:%M"
        time = datetime.now()
        the_time = time.strftime(date_format)
        othertime = ctx.message.created_at
        other_time = othertime.strftime(date_format)
        #a = datetime.strptime(time, date_format)
        #b = datetime.strptime(othertime, date_format)
        #c = datetime.now()
        #d= datetime.strptime('093000', '%H%M%S')        #Only for time comparison if someone need it.
        #e= datetime.strptime('093000', '%H%M%S')
        #delta = c - b  # Difference between time(s); you can play with a,b and c here since they are in same format
        #gr=d==e # Comparison operator on time if needed can use (>, <, >=, <= and == etc.); time only
        #fr=c>=b # Comparison operator on time if needed can use (>, <, >=, <= and == etc.); date and time                  
        #days = delta.days
        #del_sec = delta.seconds
        now = calendar.timegm(datetime.utcnow().utctimetuple())
        raff = await self.db.guild(guild).Raffle.all()
        remaining = raff["Timestamp"] - now
        #if remaining <= 0:
            #do something
            
        timer = self.time_converter(timer)
        end = calendar.timegm(ctx.message.created_at.utctimetuple()) + timer
        fmt_end = time.strftime("%a %d %b %Y %H:%M:%S", time.gmtime(end))
        await ctx.send(f"time now {the_time},message created at {other_time}, and this is the future{furure}")
        
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
        