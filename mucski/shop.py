from .randomstuff import shoplist
from .randomstuff import petlist

class Shop:
    
    async def shop(self, ctx):
        e = discord.Embed()
        e.set_author(name=f"{ctx.author.name}'s shop list", icon_url=ctx.author.avatar_url)
        e.set_thumbnail(url=ctx.bot.user.avatar_url)
        for k, v in petlist.items():
            e.add_field(name=f"{v['emoji']} {k.capitalize()}", value=f"{v['description']} - Price: {v['price']}")
        for k, v in shoplist.items():
            e.add_field(name=f"{k.capitalize()}", value=f"{v['description']}, this is a {v['type']} - Price {v['price']}")
        return await ctx.send(embed=e)
    
    @shop.group(name="buy")
    async def buy(self, ctx):
        pass
    
    @buy.command()
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
            await self.conf.user(ctx.author).pets.happiness.set(100)
            await self.conf.user(ctx.author).pets.type.set(item.lower())
            await ctx.send(f" congrats you own {item} now, take good care of it ")
            
    @buy.command()
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
            await self.conf.user(ctx.author).items.pet_food.item.set(item.lower())
            await self.conf.user(ctx.author).items.pet_food.quantity.set(quantity)
            await ctx.send(f"You just bought {quantity} of {item.lower()}")
        else:
            await self.conf.user(ctx.author).items.toys.item.set(item.lower())
            await self.conf.user(ctx.author).items.toys.quantity.set(quantity)
            await ctx.send(f"You just bought {quantity} of {item.lower()}")
        
    @shop.command()
    async def sell(self, ctx, item):
        pass
    
    @shop.command()
    async def info(self, ctx, item):
        pass
    