import discord
from datetime import datetime, timedelta
from redbot.core import commands, checks

class Mucski(commands.Cog):
    def _init_(self, bot):
        self.conf = Config.get_conf(self, 7393748858272738586)
        defaults  = {
            "cookies": 0,
            "daily_stamp": 0,
            "steal_stamp": 0,
            "work_stamp": 0,
            "pet_stamp": 0,
            "pet": {
                "name": None,
                "type": None,
                "hunger": 0,
                "happy": 0,
                "mission": False,
            },
            "item": {
                "food": {
                    "items": None,
                    "quantity": 0,
                },
                "toy": {
                    "items": None,
                    "quantity": 0,
                },
            },
        }
        self.conf.register_user(**defaults)
        
    @commands.group(name="cookie", aliases=['c'])
    @commands.guild_only()
    async def cookie(self, ctx):
        pass
    
    @cookie.command()
    async def balance(self, ctx, member: discord.Member=None):
        pass
    
    @cookie.command()
    async def profile(self, ctx):
        pass
    
    @cookie.command()
    async def work(self, ctx):
        pass
    
    @cookie.command()
    async def steal(self, ctx):
        pass
    
    @cookie.command()
    async def search(self, ctx):
        pass
    
    @cookie.command()
    async def leaderboard(self, ctx):
        pass
    
    @cookie.group(name="set")
    @checks.is_owner()
    async def set(self, ctx):
        pass
    
    @set.command()
    async def cleardb(self, ctx):
        pass
    
    @set.command()
    async def addcookie(self, ctx):
        pass
    
    @set.command()
    async def delcookie(self, ctx):
        pass
    
