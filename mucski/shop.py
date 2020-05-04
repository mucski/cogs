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
        if cookie < 0:
            return await ctx.send("Error")
        else:
            pet_type = animal.lower()
            await self.conf.user(ctx.author).pet.set_raw(
                pet_type, value = {'owned': True, 'name': animal.capitalize(), 'hunger': 100, 'happy': 100, 'mission': False}
            )
            await self.conf.user(ctx.author).cookies.set(cookie)
            #await self.conf.user(ctx.author).pet.owned.set(True)
            #await self.conf.user(ctx.author).pet.name.set(animal.capitalize())
            #await self.conf.user(ctx.author).pet.hunger.set(100)
            #await self.conf.user(ctx.author).pet.happy.set(100)
            #await self.conf.user(ctx.author).pet.type.set(animal.lower())
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
    