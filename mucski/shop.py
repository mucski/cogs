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
            #build embed
            e = discord.Embed()
            e.add_field("Pet", value=k)
            e.add_field("Description", value=v['description'])
            e.add_field("Price", value=v['price'])
            e.add_field("Price", value=v['emoji'])
            await ctx.send(embed=e)
            
        