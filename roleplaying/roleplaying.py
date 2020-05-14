import discord
from redbot.core import commands
from .randomstuff import slaplist, huglist, punchlist, sadlist, patlist, kisslist
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
        if member is None:
            member = "self."
        else:
            member = member.mention
        e.set_author(name=f"{ctx.author} kisses {member}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)
        
    