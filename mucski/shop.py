import discord

from redbot.core import commands, checks
from .randomstuff import shoplist
from .randomstuff import petlist

class Shop(commands.Cog):
    
    @commands.group(name="shop")
    async def shop(self, ctx):
        e = discord.Embed()
        for pet in petlist.keys():
            e.add_field(name=petlist['pet'], value=petlist['pet']['description'])
            e.add_field(name="price", value=petlist['pet']['price'])
        await ctx.send(embed=e)

    @shop.command()
    async def buy(self, ctx, item):
        pass
    
    @shop.command()
    async def sell(self, ctx, item):
        pass
    
    @shop.command()
    async def info(self, ctx, item):
        pass
    