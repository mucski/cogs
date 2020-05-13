import discord
from redbot.core import commands
from .randomstuff import slaplist
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