import discord
from discord import ui
from redbot.core import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot