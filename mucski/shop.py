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
        e = discord.Embed()
        e.set_author(name="Pet shop", icon_url=ctx.guild.icon_url)
        e.set_thumbnail(url="https://previews.123rf.com/images/aleksandrax/aleksandrax1704/aleksandrax170400024/76191652-logo-for-pet-shop-veterinary-clinic-animal-shelter-designed-in-a-modern-style-vector-lines-.jpg")
        e.set_footer(text="Buy and own a pet from the above list with .pet buy petname")
        for k, v in petlist.items():
            #build embed
            e.add_field(name="Pet", value=k)
            e.add_field(name="Description", value=v['description'])
            e.add_field(name="Price", value=v['price'])
            e.add_field(name="Emoji", value=v['emoji'])
        await ctx.send(embed=e)
            
        