import discord

from redbot.core import checks, commands, Config

from .shop import Shop
from .adminutils import AdminUtils
from .games import Games
from .main import Main

class Mucski(commands.Cog):
    def __init__(self, bot):
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
    async def profile(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        await Main.profile(self, ctx, member)
    
    @cookie.command()
    async def work(self, ctx):
        await Main.work(self, ctx)
    
    @cookie.command()
    async def steal(self, ctx, member: discord.Member):
        await Games.steal(self, ctx, member)
    
    @cookie.command()
    async def search(self, ctx):
        await Main.search(self, ctx)
    
    @cookie.command(name="leaderboard", aliases=['lb'])
    async def leaderboard(self, ctx):
        await Main.leaderboard(self, ctx)
    
    @cookie.command()
    async def gamble(self, ctx, amt):
        await Games.gamble(self, ctx, amt)
    
    @cookie.command()
    async def daily(self, ctx):
        await Main.daily(self, ctx)
    
    @cookie.group(name="set")
    @checks.is_owner()
    async def set(self, ctx):
        pass
    
    @set.command()
    async def cleardb(self, ctx):
        pass
    
    @set.command()
    async def addcookie(self, ctx, amt: int, member: discord.Member=None):
        if member is None:
            member = ctx.author
        await AdminUtils.add_cookie(self, ctx, amt, member)
    
    @set.command()
    async def delcookie(self, ctx):
        pass
    
    @cookie.group(name="shop")
    async def shop(self, ctx):
        pass
    
    @shop.command()
    async def items(self, ctx):
        await Shop.item(self, ctx)
    
    @shop.command()
    async def pets(self, ctx):
        await Shop.pet(self, ctx)
    
    @shop.group(name="buy")
    async def buy(self, ctx):
        pass
    
    @buy.command()
    async def pet(self, ctx):
        pass
    
    @buy.command()
    async def item(self, ctx):
        pass
    
    
