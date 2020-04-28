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
    
    
    #Get thet bot color for embeds 'await self.color(ctx)'
    async def color(self, ctx):
        return await ctx.bot.get_embed_color(location=ctx.channel)
    
    @commands.command(name="emote", aliases=['emoji'])
    async def emote(self, ctx, emoji: discord.PartialEmoji):
        e = discord.Embed(color=await self.color(ctx))
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
        e = discord.Embed(color=await self.color(ctx))
        e.set_image(url=msg)
        await ctx.send(embed=e)
        
    @commands.command(name="avatar", aliases=['pfp'])
    async def avatar(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        e = discord.Embed(color=await self.color(ctx))
        e.set_image(url=member.avatar_url)
        await ctx.send(embed=e)
        
    @commands.command()
    async def test(self, ctx):
        async for message in message.history(limit=5):
            delta = datetime.datetime.utcnow() - message.created_at
        msg="this is a test done on {}".format(delta)
        await ctx.send(msg)
        
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
        e = discord.Embed(title="Roll the dice.", color=await self.color(ctx), type='rich')
        e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        e.set_thumbnail(url=ctx.bot.user.avatar_url)
        e.add_field(name="You rolled", value=f"{you}")
        e.add_field(name="Dealer rolled", value=f"{him}")
        e.add_field(name="Dealer says:", value=f"{msg}")
        e.set_footer(text=datetime.utcnow())
        await ctx.send(embed=e)
        