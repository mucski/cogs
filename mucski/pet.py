import discord
from redbot.core import commands, checks

class Pet(commands.Cog):
    
    @commands.group()
    async def pet(self, ctx):
        pass
    
    @pet.command()
    async def buy(self, ctx, pet: str):
        name = pet
        async with self.conf.user(ctx.author).pets() as pet:
            pet["owned"] = True
            pet["name"] = name.capitalize()
            pet["mission"] = False
            pet["hunger"] = 100
            pet["happy"] = 100
            pet["clean"] = 100
            pet["type"] = name.lower()
        await ctx.send(f"You bought {pet}")