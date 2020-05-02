import discord

from redbot.core import commands, checks
from .randomstuff import shoplist
from .randomstuff import petlist

class Shop(commands.Cog):
    
    @commands.group(name="shop")
    async def shop(self, ctx):
        e = discord.Embed()
        e.set_author(name=f"{ctx.author.name}'s shop list                     ", icon_url=ctx.author.avatar_url)
        for k, v in petlist.items():
            e.add_field(name=f"{k}", value=f"{v['description']}\nPrice: {v['price']}")
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
    