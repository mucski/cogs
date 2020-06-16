import discord
from redbot.core import commands
from redbot.core.utils.predicates import MessagePredicate
import random
from textwrap import dedent
import random
from words import words, words2

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def whoami(self, ctx):
        words = random.choice(words)
        words2 = random.choice(words2)
        await ctx.send(f"{words} {words2}")
