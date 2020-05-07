import aiohttp
import discord
from redbot.core import commands, Config

class Paladins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        