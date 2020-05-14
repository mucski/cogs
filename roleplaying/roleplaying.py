import discord
from redbot.core import commands
from .randomstuff import slaplist, huglist, punchlist, sadlist, patlist, kisslist
import random

class Roleplaying(commands.Cog):
    """Simple roleplaying cog by mucski"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def slap(self, ctx, member: discord.Member = None):
        img = random.choice(slaplist)
        embed = discord.Embed()
        if member is None or member == ctx.author:
            embed.set_author(name=f"{ctx.author.name} slaps himself.", icon_url=ctx.author.avatar_url)
        else:
            embed.set_author(name=f"{ctx.author.name} slaps {member.name}", icon_url=ctx.author.avatar_url)
        embed.set_image(url=img)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def kiss(self, ctx, member: discord.Member = None):
        img = random.choice(kisslist)
        e = discord.Embed()
        e.set_image(url=imgurl)
        if member is None:
            member = "mirror."
        else:
            member = member.name
        e.set_author(name=f"{ctx.author} kisses {member}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)
        
    @commands.command()
    async def pat(self, ctx, member: discord.Member = None):
        img = random.choice(patlist)
        embed = discord.Embed()
        if member is None or member == ctx.author:
            embed.set_author(name=f"{ctx.author.name} pats himself/herself.", icon_url=ctx.author.avatar_url)
        else:
            embed.set_author(name=f"{ctx.author.name} pats {member.name}", icon_url=ctx.author.avatar_url)
        embed.set_image(url=img)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def punch(self, ctx, member: discord.Member = None):
        img = random.choice(punchlist)
        embed = discord.Embed()
        if member is None or member == ctx.author:
            embed.set_footer(text="the air.")
        else:
            embed.set_footer(text=f"{member.mention}")
        embed.set_author(name=f"{ctx.author.name} punches", icon_url=ctx.author.avatar_url)
        embed.set_image(url=img)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def hug(self, ctx, member: discord.Member = None):
        img = random.choice(huglist)
        embed = discord.Embed()
        if member is None or member == ctx.author:
            embed.set_author(name=f"{ctx.author.name} hugs himself/herself.", icon_url=ctx.author.avatar_url)
        else:
            embed.set_author(name=f"{ctx.author.name} hugs {member.name}", icon_url=ctx.author.avatar_url)
        embed.set_image(url=img)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def sad(self, ctx):
        img = random.choice(sadlist)
        embed = discord.Embed()
        embed.set_author(name=f"{ctx.author.name} is sad.", icon_url=ctx.author.avatar_url)
        embed.set_image(url=img)
        await ctx.send(embed=embed)