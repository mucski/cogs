import discord
from redbot.core import commands
from redbot.core.utils.predicates import MessagePredicate
import random
from textwrap import dedent
from .markov import Markov

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        w = Markov(" ", 2)
        w.learn("the quick brown fox jumps over the lazy dog")

    @commands.command()
    async def story(ctx):
        story = w.query()
        await ctx.send(story)