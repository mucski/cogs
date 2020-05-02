import discord

from redbot.core import commands, checks
from .randomstuff import shoplist
from .randomstuff import petlist

class Shop(commands.Cog):
    
    @commands.group(name="shop")
    async def shop(self, ctx):
        for pet in petlist:
            shop = petlist.keys()
        await ctx.send(shop)

    @shop.command()
    async def buy(self, ctx, item):
        pass
    
    @shop.command()
    async def sell(self, ctx, item):
        pass
    
    @shop.command()
    async def info(self, ctx, item):
        pass
    