import discord
from redbot.core import commands, Config

class Coin(commands.Cog):
    """Coin Tycoon, developed by Mucski"""
    def __init__(self, bot):
        self.bot = bot
        self.db = Config.get_conf(self, 9408453854, force_registration=True)

        default_user = {
            "data": {}
        }
        default_guild = {
            "data_guild": {}
        }
        self.db.register_user(**default_user)
        self.db.register_guild(**default_guild)