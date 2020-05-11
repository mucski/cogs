import discord
from redbot.core import commands, checks
from .randomstuff import petlist

class Pet(commands.Cog):
    
    @commands.group()
    async def pet(self, ctx):
        pass
    
    @pet.command()
    async def buy(self, ctx, pet: str):
        price = petlist[pet]["price"]
        name = pet
        coins = await self.conf.user(ctx.author).coins()
        if await self.conf.user(ctx.author).pets():
            await ctx.send("You already own a pet. Currently you can only have 1 pet.")
            return
        async with self.conf.user(ctx.author).pets() as pet:
            pet["owned"] = True
            pet["name"] = name.capitalize()
            pet["mission"] = False
            pet["hunger"] = 100
            pet["happy"] = 100
            pet["clean"] = 100
            pet["type"] = name.lower()
        coins -= price
        if coins <= 0:
            await ctx.send("Not enough coins to buy a pet, sorry.")
            return
        await self.conf.user(ctx.author).coins.set(coins)
        await ctx.send(f"You bought {pet}")
        
    @pet.command()
    async def info(self, ctx):
        if not self.conf.user(ctx.author).pets():
            await ctx.send("You dont own any pets.")
            return
        async with self.conf.user(ctx.author).pets() as pet:
            e = discord.Embed()
            e.add_field(name="Name", value=pet["name"])
            e.add_field(name="Type", value=pet["type"])
            e.add_field(name="Hunger", value=pet["hunger"])
            e.add_field(name="Happy", value=pet["happy"])
            e.add_field(name="Clean", value=pet["clean"])
            if pet["mission"] == True:
                e.add_field(name="On Mission", value="Yes, remaining:")
            else:
                e.add_field(name="On Mission", value="Nope")
            await ctx.send(embed=e)