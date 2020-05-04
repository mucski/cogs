import discord

from redbot.core import checks, commands, Config

from .shop import Shop
from .adminutils import AdminUtils
from .games import Games
from .main import Main
from .pet import Pet

class Mucski(commands.Cog):
    def __init__(self, bot):
        self.conf = Config.get_conf(self, 7393748858272738586)
        defaults  = {
            "cookies": 0,
            "daily_stamp": 0,
            "steal_stamp": 0,
            "work_stamp": 0,
            "pet_stamp": 0,
            "pet": {},
            "item": {
                "food": {},
                "toy": {},
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
        await AdminUtils.reset_db(self, ctx)
    
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
        await Shop.items(self, ctx)
    
    @shop.command()
    async def pets(self, ctx):
        await Shop.pets(self, ctx)
    
    @shop.group(name="buy")
    async def buy(self, ctx):
        pass
    
    @buy.command()
    async def animal(self, ctx, pet: str):
        await Shop.animal(self, ctx, pet)
    
    @buy.command()
    async def item(self, ctx, item: str, quantity: int):
        await Shop.item(self, ctx, item, quantity)
        
    
    @cookie.group(name="pet")
    async def pet(self, ctx):
        pass
    
    @pet.command()
    async def info(self, ctx):
        await Pet.info(self, ctx)
    
    @pet.command()
    async def adventure(self, ctx):
        await Pet.adventure(self, ctx)
    
    @pet.command()
    async def feed(self, ctx):
        pass
    
    @pet.command()
    async def play(self, ctx):
        pass
    
    @pet.command()
    async def abandon(self, ctx):
        pass
    
    @pet.command()
    async def rename(self, ctx, *, name: str):
        await Pet.rename(self, ctx, name)
        
    
