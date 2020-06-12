import discord
from redbot.core import commands
from redbot.core.utils.predicates import MessagePredicate
import random
from textwrap import dedent
from .markov import Markov

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.w = Markov(" ", 2)
        self.w.learn("the quick brown fox jumps over the lazy dog {} wtf is this shit no matter what I type here it just gives it back in the same order with nothing changed so I am not even sure what the fuck to input here don't sweat this is just a test to see if it changes and what is this I don't know")

    @commands.command()
    async def story(self, ctx):
        story = self.w.query()
        await ctx.send(story.format(ctx.author))