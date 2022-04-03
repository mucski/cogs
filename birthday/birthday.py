import discord
from redbot.core import commands, Config, checks


class Birthday(commands.Cog):
    """Birthday cog by Mucski hehehee"""
    def __init__(self, bot):
        self.bot = bot


    @commands.group()
    async def birthday(self, ctx):
        """Under cumstruction"""
        await ctx.send("Under construction")
