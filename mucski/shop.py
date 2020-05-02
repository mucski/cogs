import discord

from redbot.core import commands, checks

class Shop(commands.Cog):
    
    @commands.group(name="shop")
    async def shop(self, ctx):
        pass

    @shop.command()
    async def buy(self, ctx, item):
        pass
    
    @shop.command()
    async def sell(self, ctx, item):
        pass
    
    @shop.command()
    async def info(self, ctx, item):
        pass
    