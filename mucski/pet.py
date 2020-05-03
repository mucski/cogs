import discord
import random
import asyncio
from datetime import datetime, timedelta

from redbot.core import commands, checks
from .randomstuff import doggo_responses
from redbot.core.utils.chat_formatting import humanize_timedelta

class Pet(commands.Cog):
    
    @commands.group(name="pet")
    async def pet(self, ctx):
        pass
    
    @pet.command()
    async def send(self, ctx):
        now = datetime.utcnow().replace(microsecond=0)
        time = random.randint(900,3600)
        timer = timedelta(seconds=time)
        pet_stamp = await self.conf.user(ctx.author).pet_stamp()
        pet_stamp = datetime.fromtimestamp(pet_stamp)
        wait = pet_stamp - now
        next_stamp = timer + now
        on_mission = await self.conf.user(ctx.author).pets.mission()
        if on_mission is True:
            return await ctx.send(f"already in a mission {humanize_timedelta(timedelta=wait)}")
        else:
            await ctx.send(f"sent your dumb pet on an adventure for {time} seconds")
            await self.conf.user(ctx.author).pets.mission.set(True)
            await self.conf.user(ctx.author).pet_stamp.set(next_stamp.timestamp())
            await asyncio.sleep(time)
            responses = random.choice(doggo_responses)
            await ctx.send(responses)
            await self.conf.user(ctx.author).pets.mission.set(False)
        
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
    
