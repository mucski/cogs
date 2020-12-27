from redbot.core import commands
import random

class Test2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def key(self, ctx):
        f = open("/home/music166/mucski/key.txt", "r")
        auth = f.readline()
        devid = f.readline()
        await ctx.send(f"This is the dev id {devid} and this is the author key {auth}")
        f.close()