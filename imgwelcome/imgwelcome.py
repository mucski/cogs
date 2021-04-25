# Image Manipulation
from PIL import Image, ImageDraw, ImageOps

# Discord
import discord

# Redbot
from redbot.core import commands, checks

class Imgwelcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def imgsetup(self, ctx):
        pass

    @commands.command()
    async def imgpreview(self, ctx):
        pass