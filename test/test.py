from redbot.core import commands

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Gello World 🌍")