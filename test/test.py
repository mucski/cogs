from redbot.core import commands
import random


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def test(self, ctx):
        pass

    @test.command()
    async def lockpick(self, ctx, number: int):
        chars = "◀▶"
        #lock_length = 10
        lock = ''.join(random.choice(chars) for _ in range(number))
        await ctx.send(lock)