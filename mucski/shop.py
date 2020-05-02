import discord

from redbot.core import commands, checks

class Shop(commands.Cog):
    
    @commands.group(name="shop")
    async def shop(self, ctx):
        pass

    @shop.commands()
    async def buy(self, ctx, item):
        pass
    
    @shop.commands()
    async def sell(self, ctx, item):
        pass
    
    @shop.commands()
    async def info(self, ctx, item):
        pass
    