from redbot.core import commands
from redbot.core.utils.predicates import MessagePredicate
import random

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def lockpick(self, ctx):
        #Create the code
        lock = []
        
        first = lock.append(str(random.randint(0, 9)))
        second = lock.append(str(random.randint(0, 9)))
        third = lock.append(str(random.randint(0, 9)))
        
        safe_lock = ''.join(lock)
        
        
        await ctx.send(safe_lock)