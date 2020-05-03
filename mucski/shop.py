import discord

from .randomstuff import shoplist
from .randomstuff import petlist

class Shop:
    
    async def pets(self, ctx):
        e = discord.Embed()
        e.set_author(name=f"{ctx.author.name} pet list", icon_url=ctx.author.avatar_url)
        e.set_thumbnail(url=ctx.bot.user.avatar_url)
        for k, v in petlist.items():
            e.add_field(name=f"{v['emoji']} {k.capitalize()}", value=f"{v['description']} - Price: {v['price']}")
        return await ctx.send(embed=e)
    
    async def items(self, ctx):
        e = discord.Embed()
        e.set_author(name=f"{ctx.author.name} item shop", icon_url=ctx.author.avatar_url)
        e.set_thumbnail(url=ctx.bot.user.avatar_url)
        for k, v in shoplist.items():
            e.add_field(name=f"{k.capitalize()} - {v['type']}", value=f"{v['description']} - Price {v['price']}")
        await ctx.send(embed=e)
    
    async def pet(self, ctx, item: str):
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
            await self.conf.user(ctx.author).pets.happy.set(100)
            await self.conf.user(ctx.author).pets.type.set(item.lower())
            await ctx.send(f" congrats you own {item} now, take good care of it ")
            
    async def item(self, ctx, item: str, quantity: int):
        if item.lower() in shoplist.keys():
            value = shoplist[item]['price']
        else:
            return await ctx.send("no such item")
        cookie = await self.conf.user(ctx.author).cookies()
        cookie -= value
        if cookie < value:
            return await ctx.send("Need more cookies")
        elif shoplist[item]['type'] == "food":
            await self.conf.user(ctx.author).item.food.items.set(item.lower())
            await self.conf.user(ctx.author).item.food.quantity.set(quantity)
            await ctx.send(f"You just bought {quantity} of {item.lower()}")
        else:
            await self.conf.user(ctx.author).item.toys.items.set(item.lower())
            await self.conf.user(ctx.author).item.toys.quantity.set(quantity)
            await ctx.send(f"You just bought {quantity} of {item.lower()}")
        
    async def sell(self, ctx, item):
        pass
    
    async def info(self, ctx, item):
        pass
    