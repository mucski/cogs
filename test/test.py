from redbot.core import commands
import random
from .words import words, words2
import aiohttp
from PIL import Image, ImageDraw
from functools import partial
from IO import BytesIO

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def whoami(self, ctx):
        word = random.choice(words)
        word2 = random.choice(words2)
        await ctx.send(f"{word} {word2}")