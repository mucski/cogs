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
        return await ctx.send(embed=e)
    
    async def animal(self, ctx, animal):
        if animal.lower() in petlist.keys():
            value = petlist[animal]['price']
        else:
            return await ctx.send("pet doesnt exist")
        cookie = await self.conf.user(ctx.author).cookies()
        cookie -= value
        if cookie <= 0:
            return await ctx.send("Error")
        else:
            pet_type = animal.lower()
            await self.conf.user(ctx.author).pet.set_raw(
                value = {'type': pet_type, 'name': animal.capitalize(), 'hunger': 100, 'happy': 100, 'mission': False}
            )
            await self.conf.user(ctx.author).cookies.set(cookie)
            return await ctx.send(f" congrats you own {animal} now, take good care of it ")
            
    async def item(self, ctx, item, quantity):
        if item.lower() in shoplist.keys():
            value = shoplist[item]['price']
        else:
            return await ctx.send("no such item")
        cookie = await self.conf.user(ctx.author).cookies()
        cookie -= value
        if cookie < value:
            return await ctx.send("Need more cookies")
        type = shoplist[item]['type']
        item = item.lower()
        if quantity == 0:
            quantity = 1
        if type == 'food':
            await self.conf.user(ctx.author).item.food.set_raw(
                value = {item: quantity}
            )
        else:
            await self.conf.user(ctx.author).item.toy.set_raw(
                value = {item: quantity}
            )
        await self.conf.user(ctx.author).cookies.set(cookie)
        await ctx.send(f"You just bought {quantity} of {item}")
        
    async def sell(self, ctx, item):
        pass
    
    async def info(self, ctx, item):
        pass
    