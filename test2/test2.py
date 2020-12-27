from redbot.core import commands
import random

class Test2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def key(self, ctx):
        f = open("key.txt", "r")
        await ctx.send(f)