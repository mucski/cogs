from redbot.core import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def test(self, ctx):
        pass

    @test.command()
    async def penis(self, ctx):
        pass
