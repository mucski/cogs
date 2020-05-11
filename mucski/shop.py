import discord
from redbot.core import commands, checks
from .randomstuff import petlist

class Shop(commands.Cog):
    #list pets
    @commands.group()
    async def shop(self, ctx):
        pass
    
    @shop.command()
    async def pets(self, ctx):
        for k, v in petlist.items():
            test = petlist[k][v]
            await ctx.send(test)
            
        