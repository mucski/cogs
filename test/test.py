from redbot.core import commands
from redbot.core.utils.predicates import MessagePredicate
import random
from textwrap import dedent

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def lockpick(self, ctx):
        #Create the code
    
        first = random.randint(0, 9)
        second = random.randint(0, 9)
        third = random.randint(0, 9)
        
        desc = """
        #############
        # - + - + - #
        # - {} - {} - {} - #
        # - + - + - #
        #############
        """.format(first, second, third)
        
        safe_lock = dedent(f"```{desc}```")
        
        await ctx.send(safe_lock)