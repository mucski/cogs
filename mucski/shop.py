import discord

from redbot.core import commands, checks
from .randomstuff import shoplist
from .randomstuff import petlist

class Shop(commands.Cog):
    
    @commands.group(name="shop")
    async def shop(self, ctx):
        e = discord.Embed()
        e.set_author(name=f"{ctx.author.name}'s shop list", icon_url=ctx.author.avatar_url)
        e.set_thumbnail(url=ctx.bot.user.avatar_url)
        for k, v in petlist.items():
            e.add_field(name=f"{v['emoji']} {k.capitalize()}", value=f"{v['description']}\nPrice: {v['price']}")
        for k, v in shoplist.items():
            e.add_field(name=f"{k.capitalize()}", value=f"{v['description']}, this is a {v['type']}\n Price {v['price']}")
        await ctx.send(embed=e)

    @shop.command()
    async def buy(self, ctx, item: str):
        if item.lower() in petlist.keys():
            value = petlist[item]['price']
        else:
            return await ctx.send("pet doesnt exist")
        cookie = await self.conf.user(ctx.author).cookies()
        cookie -= value
        if cookie < 0:
            return await ctx.send("Error")
        else:
            await self.conf.user(ctx.author).cookies.set(cookie)
            await self.conf.user(ctx.author).pets.owned.set(True)
            await self.conf.user(ctx.author).pets.name.set(item)
            await self.conf.user(ctx.author).pets.hunger.set(100)
            await self.conf.user(ctx.author).pets.happiness.set(100)
            await self.conf.user(ctx.author).pets.type.set(item.lower())
            await ctx.send(f" congrats you own {item} now, take good care of it ")
        
            
    
    @shop.command()
    async def sell(self, ctx, item):
        pass
    
    @shop.command()
    async def info(self, ctx, item):
        pass
    