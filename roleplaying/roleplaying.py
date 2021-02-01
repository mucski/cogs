import discord
from redbot.core import commands
from .randomstuff import punchlist, kisslist, cuddlelist, huglist, patlist, slaplist, sadlist
import random

class Roleplaying(commands.Cog):
    """Simple roleplaying cog by mucski"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def kiss(self, ctx, member: discord.Member = None):
        if ctx.author.nick not None:
            authnick = ctx.author.nick
        else
            authnick = ctx.author.name
        if member.nick not None:
            memnick = member.nick
        else
            memnick = member.name
        img = random.choice(kisslist)
        e = discord.Embed()
        e.set_image(url=img)
        e.set_author(name=f"{} kisses:", icon_url=ctx.author.avatar_url)
        if member is None:
            e.set_footer(text="the air.")
        else:
            e.set_footer(text=member.name)
        await ctx.send(embed=e)
        
    @commands.command()
    async def punch(self, ctx, member: discord.Member = None):
        img = random.choice(punchlist)
        e = discord.Embed()
        e.set_image(url=img)
        e.set_author(name=f"{ctx.author.name} punches:", icon_url=ctx.author.avatar_url)
        if member is None:
            e.set_footer(text="the air.")
        else:
            e.set_footer(text=member.name)
        await ctx.send(embed=e)
        
    @commands.command()
    async def cuddle(self, ctx, member: discord.Member = None):
        img = random.choice(cuddlelist)
        e = discord.Embed()
        e.set_image(url=img)
        e.set_author(name=f"{ctx.author.name} cudles with:", icon_url=ctx.author.avatar_url)
        if member is None:
            e.set_footer(text="the air.")
        else:
            e.set_footer(text=member.name)
        await ctx.send(embed=e)
        
    @commands.command()
    async def hug(self, ctx, member: discord.Member = None):
        img = random.choice(huglist)
        e = discord.Embed()
        e.set_image(url=img)
        e.set_author(name=f"{ctx.author.name} hugs:", icon_url=ctx.author.avatar_url)
        if member is None:
            e.set_footer(text="the air.")
        else:
            e.set_footer(text=member.name)
        await ctx.send(embed=e)
        
    @commands.command()
    async def pat(self, ctx, member: discord.Member = None):
        img = random.choice(patlist)
        e = discord.Embed()
        e.set_image(url=img)
        e.set_author(name=f"{ctx.author.name} pats:", icon_url=ctx.author.avatar_url)
        if member is None:
            e.set_footer(text="the air.")
        else:
            e.set_footer(text=member.name)
        await ctx.send(embed=e)
        
    @commands.command()
    async def slap(self, ctx, member: discord.Member = None):
        img = random.choice(slaplist)
        e = discord.Embed()
        e.set_image(url=img)
        e.set_author(name=f"{ctx.author.name} slaps", icon_url=ctx.author.avatar_url)
        if member is None:
            e.set_footer(text="the air.")
        else:
            e.set_footer(text=member.name)
        await ctx.send(embed=e)
        
    @commands.command()
    async def sad(self, ctx):
        img = random.choice(sadlist)
        e = discord.Embed()
        e.set_image(url=img)
        e.set_author(name=f"{ctx.author.name} is sad.", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)
    