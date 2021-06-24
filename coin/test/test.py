from redbot.core import commands


class Test(commands.Cog):
    """ Mucski's test cog. """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        pass

    @test.command()
    async def penis(self, ctx):
        pass
