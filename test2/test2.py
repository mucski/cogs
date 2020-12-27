from redbot.core import commands
import random
from discord import File

from PIL import Image, ImageDraw, ImageFont
import io

class Test2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test2(self, ctx):
        text = "Hello I am a test text"
        image = ""