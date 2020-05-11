import asyncio
import discord
import itertools
import math
import random
import time
import re
from discord.ext import tasks, commands
from datetime import datetime, timedelta

from redbot.core import bank, checks, commands, Config
from redbot.core.utils.chat_formatting import bold, box, humanize_list, humanize_number, pagify, humanize_timedelta
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core.utils.predicates import MessagePredicate
from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions


class Mucski2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, 282828485)
        defaults = {
            "gold": 0,
            "datetime": "",
            "daily_stamp": 0,
            "daily_timer": 0,
            "vip_stamp": 0,
        }
        default_guild = {
            "vip_timer": 0,
            #"hunt_interval_maximum": 3600,
            #"wait_for_bang_timeout": 20,
            "channel": 0,
            "message":0,
        }
        default_user = {"author_name": None, "score": {}, "total": 0}
        self.conf.register_user(**defaults)
        self.conf.register_guild(**default_guild)

    
    #Get thet bot color for embeds 'await self.color(ctx)'
    async def color(self, ctx):
        return await ctx.bot.get_embed_color(location=ctx.channel)
    
    @commands.command(name="emote", aliases=['emoji'])
    async def emote(self, ctx, emoji: discord.PartialEmoji):
        await ctx.send(emoji.url)
        
    @commands.group(name="vip")
    @checks.is_owner()
    async def vip(self, ctx):
        pass
    
    @vip.command()
    async def start(self, ctx, channel: discord.TextChannel=None, *, text="Daily ☢️V.I.P Supreme☢️ giveaway.\nReact bellow to enter 💎", time=5):
        if channel == None:
            channel = ctx.channel
        e = discord.Embed(color=await self.bot.get_embed_color(ctx), description=text)
        e.set_author(name=f"{self.bot.user.name}' giveaway", icon_url=self.bot.user.avatar_url)
        e.set_footer(text=f"Giveaway code by Mucski | giveaway will run for {time}")
        msg = await channel.send(embed=e)
        await msg.add_reaction("💎")
        await self.conf.guild(ctx.guild).channel.set(channel.id)
        await self.conf.guild(ctx.guild).message.set(msg.id)
        await self.conf.guild(ctx.guild).vip_timer.set(time)
        #automation
        asyncio.sleep(time)
        await self._stop(ctx)
            
    #@vip.command()
    async def _stop(self, ctx):
        msg = await self.conf.guild(ctx.guild).message()
        channel = await self.conf.guild(ctx.guild).channel()
        if not channel:
            await ctx.send("Start a new giveaway")
            return
        channel = self.bot.get_channel(channel)
        if msg:
            message = await channel.fetch_message(msg)
        else:
            await ctx.send("Message deleted or doesnt exist")
            return
        users = []
        async for user in message.reactions[0].users():
            if user == self.bot.user:
                continue
            users.append(user)
        await self.conf.guild(ctx.guild).channel.clear()
        await self.conf.guild(ctx.guild).message.clear()
        a = discord.Embed(color=await self.bot.get_embed_color(ctx), description="Give away finished, and the winner is:\nSee bellow for winner.")
        a.set_author(name=f"{self.bot.user.name}'s giveaway", icon_url=self.bot.user.avatar_url)
        a.set_footer(text="Giveaway code by Mucski")
        if not users:
            await message.edit(embed=a)
            await channel.send("There were either no entries or an error occured.")
            return
        randomize = random.choice(users)
        await message.edit(embed=a)
        await channel.send(f"The winner is {randomize.mention}, congratulations.")
    
    @commands.command()
    async def who(self, ctx, channel: discord.TextChannel, messageid: int):
        try:
            msg = await channel.fetch_message(messageid)
        except HTTPException:
            return await ctx.send("Couldn't find that message")
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
    async def rol(self, ctx):
        him = random.randint(1,6)
        you = random.randint(1,6)
        if you < 6 and him > you:
            msg = "Oops, dealer won."
        elif you == him:
            msg = "Looks like its a tie."
        elif him < 6 and you > him:
            msg = "Yay you won."
        e = discord.Embed()
        description = (
            f'You rolled: - **{you}**\n'
            f'Dealer rolled: - **{him}**\n\n'
            f'{msg}'
        )
        e.title = "Casino Royale"
        e.description = description
        e.set_author(name=f"{ctx.author.name}'s dice roll game.", icon_url=f"{ctx.author.avatar_url}")
        e.set_thumbnail(url=f"{ctx.bot.user.avatar_url}")
        e.add_field(name="Testing", value="Testing", inline=False)
        await ctx.send(embed=e)
        
        
    champions = ['Ash', 'Evie', 'Sha Lin', 'Corvus', 'Mal Damba', 'Maeve', 'Androxus', 'Lex', 'Fernando', 'Jenos', 'Furia', 'Viktor', 'Skye', 'Ruckus', 'Zhin', 'Tyra', 'Khan', 'Atlas', 'Makoa', 'Raum', 'Tiberius', 'Bomb King', 'Drogoz', 'Moji', 'Seris', 'Grover', 'Io', 'Dredge', 'Imani', 'Vivian']
    
    @commands.command()
    async def randomchamp(self, ctx):
        champ = random.choice(self.champions)
        await ctx.send(f"You should play with **{champ}** now, hehe.")
    