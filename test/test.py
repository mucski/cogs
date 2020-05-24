from redbot.core import commands
from redbot.core.utils.predicates import MessagePredicate
import random

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def lockpick(self, ctx):
        #Create the code
        first = random.randint(0, 9)
        second = random.randint(0, 9)
        third = random.randint(0, 9)
        
        safe_lock = first + second + third
        
        await ctx.send(safe_lock)