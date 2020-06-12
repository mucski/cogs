import discord
from redbot.core import commands
from redbot.core.utils.predicates import MessagePredicate
import random
from textwrap import dedent
from .markov import Markov

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.w = Markov(" ", 1)
        self.w.learn_file("/home/music166/.local/share/Red-DiscordBot/data/red/cogs/CogManager/cogs/test/dictionary.txt")

    @commands.command()
    async def ask(self, ctx, ask):
        story = self.w.ask(ask)
        await ctx.send(story.format(ctx.author))