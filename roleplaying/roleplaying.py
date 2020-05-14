import discord
from redbot.core import commands
from .randomstuff import slaplist, huglist, punchlist, sadlist, patlist, kisslist, cuddlelist
import random

class Roleplaying(commands.Cog):
    """Simple roleplaying cog by mucski"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def kiss(self, ctx, member: discord.Member = None):
        img = random.choice(kisslist)
        e = discord.Embed()
        e.set_image(url=img)
        e.set_author(name=f"{ctx.author.name} kisses:", icon_url=ctx.author.avatar_url)
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
    async def cudle(self, ctx, member: discord.Member = None):
        img = random.choice(cudlelist)
        e = discord.Embed()
        e.set_image(url=img)
        e.set_author(name=f"{ctx.author.name} cudles with:", icon_url=ctx.author.avatar_url)
        if member is None:
            e.set_footer(text="the air.")
        else:
            e.set_footer(text=member.name)
        await ctx.send(embed=e)
        
    