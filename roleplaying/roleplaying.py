import discord
from redbot.core import commands
from .randomstuff import slaplist, huglist, punchlist, sadlist, patlist, kisslist
import random

class Roleplaying(commands.Cog):
    """Simple roleplaying cog by mucski"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def kiss(self, ctx, member: discord.Member):
        img = random.choice(kisslist)
        e = discord.Embed()
        e.set_image(url=img)
        e.set_author(name=f"{ctx.author.name} kisses:", icon_url=ctx.author.avatar_url)
        e.set_footer(text=member.name)
        await ctx.send(embed=e)
        
    