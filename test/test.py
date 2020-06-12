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
        self.w.learn_file("/words.txt")

    @commands.command()
    async def story(self, ctx):
        story = self.w.query()
        await ctx.send(story.format(ctx.author))