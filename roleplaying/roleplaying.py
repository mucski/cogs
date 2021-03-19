import discord
from redbot.core import commands
from .randomstuff import kisslist, slaplist, punchlist
from .randomstuff import cuddlelist, sadlist, patlist, huglist
import random


class Roleplaying(commands.Cog):
    """Simple roleplaying cog by mucski"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kiss(self, ctx, member: discord.Member = None):
        if ctx.author.nick is None:
            authnick = ctx.author.name
        else:
            authnick = ctx.author.nick
        if member.nick is None:
            memnick = member.name
        else:
            memnick = member.nick
        img = random.choice(kisslist)
        e = discord.Embed()
        e.set_image(url=img)
        e.set_author(name=f"{authnick} kisses:",
                     icon_url=ctx.author.avatar_url)
        if member is None:
            e.set_footer(text="the air.")
        else:
            e.set_footer(text=memnick)
        await ctx.send(embed=e)

    @commands.command()
    async def punch(self, ctx, member: discord.Member = None):
        if ctx.author.nick is None:
            authnick = ctx.author.name
        else:
            authnick = ctx.author.nick
        if member.nick is None:
            memnick = member.name
        else:
            memnick = member.nick
        img = random.choice(punchlist)
        e = discord.Embed()
        e.set_image(url=img)
        e.set_author(name=f"{authnick} punches:",
                     icon_url=ctx.author.avatar_url)
        if member is None:
            e.set_footer(text="the air.")
        else:
            e.set_footer(text=memnick)
        await ctx.send(embed=e)

    @commands.command()
    async def cuddle(self, ctx, member: discord.Member = None):
        if ctx.author.nick is None:
            authnick = ctx.author.name
        else:
            authnick = ctx.author.nick
        if member.nick is None:
            memnick = member.name
        else:
            memnick = member.nick
        img = random.choice(cuddlelist)
        e = discord.Embed()
        e.set_image(url=img)
        e.set_author(name=f"{authnick} cudles with:",
                     icon_url=ctx.author.avatar_url)
        if member is None:
            e.set_footer(text="the air.")
        else:
            e.set_footer(text=memnick)
        await ctx.send(embed=e)

    @commands.command()
    async def hug(self, ctx, member: discord.Member = None):
        if ctx.author.nick is None:
            authnick = ctx.author.name
        else:
            authnick = ctx.author.nick
        if member.nick is None:
            memnick = member.name
        else:
            memnick = member.nick
        img = random.choice(huglist)
        e = discord.Embed()
        e.set_image(url=img)
        e.set_author(name=f"{authnick} hugs:", icon_url=ctx.author.avatar_url)
        if member is None:
            e.set_footer(text="the air.")
        else:
            e.set_footer(text=memnick)
        await ctx.send(embed=e)

    @commands.command()
    async def pat(self, ctx, member: discord.Member = None):
        if ctx.author.nick is None:
            authnick = ctx.author.name
        else:
            authnick = ctx.author.nick
        if member.nick is None:
            memnick = member.name
        else:
            memnick = member.nick
        img = random.choice(patlist)
        e = discord.Embed()
        e.set_image(url=img)
        e.set_author(name=f"{authnick} pats:", icon_url=ctx.author.avatar_url)
        if member is None:
            e.set_footer(text="the air.")
        else:
            e.set_footer(text=memnick)
        await ctx.send(embed=e)

    @commands.command()
    async def slap(self, ctx, member: discord.Member = None):
        if ctx.author.nick is None:
            authnick = ctx.author.name
        else:
            authnick = ctx.author.nick
        if member.nick is None:
            memnick = member.name
        else:
            memnick = member.nick
        img = random.choice(slaplist)
        e = discord.Embed()
        e.set_image(url=img)
        e.set_author(name=f"{authnick} slaps", icon_url=ctx.author.avatar_url)
        if member is None:
            e.set_footer(text="the air.")
        else:
            e.set_footer(text=memnick)
        await ctx.send(embed=e)

    @commands.command()
    async def sad(self, ctx):
        if ctx.author.nick is None:
            authnick = ctx.author.name
        else:
            authnick = ctx.author.nick
        img = random.choice(sadlist)
        e = discord.Embed()
        e.set_image(url=img)
        e.set_author(name=f"{authnick} is sad.",
                     icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)
