import discord
from redbot.core import commands
from .randomstuff import slaplist, huglist, punchlist, sadlist, patlist, kisslist
import random

class Roleplaying(commands.Cog):
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
        embed = discord.Embed()
        if member is None or member == ctx.author:
            embed.set_author(name=f"{ctx.author.name} kisses himself/herself.", icon_url=ctx.author.avatar_url)
        else:
            embed.set_author(name=f"{ctx.author.name} kisses {member.name}", icon_url=ctx.author.avatar_url)
        embed.set_image(url=img)
        await ctx.send(embed=embed)
        
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
            embed.set_author(name=f"{ctx.author.name} punches himself/herseld.", icon_url=ctx.author.avatar_url)
        else:
            embed.set_author(name=f"{ctx.author.name} punches {member.name}", icon_url=ctx.author.avatar_url)
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