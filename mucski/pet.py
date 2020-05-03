import discord
import random
import asyncio

from redbot.core import commands, checks
from .randomstuff import doggo_responses

class Pet(commands.Cog):
    
    @commands.group(name="pet")
    async def pet(self, ctx):
        pass
    
    @pet.command()
    async def send(self, ctx):
        time = random.randint(10,50)
        on_mission = await self.conf.user(ctx.author).pets.mission()
        if on_mission:
            return await ctx.send("already in a mission")
        else:
            await ctx.send(f"sent your dumb pet on an adventure for {time} seconds")
            await self.conf.user(ctx.author).pets.mission(True)
            await asyncio.sleep(time)
            responses = random.choice(doggo_responses)
            await ctx.send(responses)
            await self.conf.user(ctx.author).pets.mission(False)
        
    @pet.command()
    async def feed(self, ctx):
        pass
    
    @pet.command()
    async def play(self, ctx):
        pass
    
    @pet.command()
    async def info(self, ctx):
        if await self.conf.user(ctx.author).pets.owned() == "None":
            await ctx.send("Get yourself a pet first.")
        else:
            health = await self.conf.user(ctx.author).pets.hunger()
            name = await self.conf.user(ctx.author).pets.name()
            happiness = await self.conf.user(ctx.author).pets.happiness()
            pettype = await self.conf.user(ctx.author).pets.type()
            e = discord.Embed()
            e.set_author(name=f"{ctx.author.name}'s {pettype}", icon_url=ctx.author.avatar_url)
            e.add_field(name="Pet health", value=health)
            e.add_field(name="Pet name", value=name.capitalize())
            e.add_field(name="Pet happynes", value=happiness)
            e.add_field(name="Pet type", value=pettype)
            await ctx.send(embed=e)
    
