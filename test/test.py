import discord
from redbot.core import commands
from redbot.core.utils.predicates import MessagePredicate
import random
from textwrap import dedent
from .markov import markov

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        w = markov.Markov(" ", 2)
        w.learn("the quick brown fox jumps over the lazy dog")

    @command.command()
    async def story(ctx):
        story = w.query()
        await ctx.send(story)