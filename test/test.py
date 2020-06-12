import discord
from redbot.core import commands
from redbot.core.utils.predicates import MessagePredicate
import random
from textwrap import dedent
from .markov import Markov

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def story(self, ctx):
        w = Markov(" ", 2)
        w.learn(f"the quick brown fox jumps over the lazy dog {ctx.author} wtf is this shit no matter what I type here it just gives it back in the same order with nothing changed so I am not even sure what the fuck to input here don't sweat this is just a test to see if it changes and what is this I don't know")
        story = w.query()
        await ctx.send(story)