import discord
import random
import asyncio
from datetime import datetime, timedelta

from redbot.core import commands, checks
from .randomstuff import doggo_responses
from redbot.core.utils.chat_formatting import humanize_timedelta

class Pet:
    async def adventure(self, ctx):
        owned = await self.conf.user(ctx.author).pet.owned()
        if owned is False:
            return await ctx.send("No pet no gain")
        now = datetime.utcnow().replace(microsecond=0)
        time = random.randint(100,500)
        pet_timer = timedelta(seconds=time)
        pet_stamp = await self.conf.user(ctx.author).pet_stamp()
        pet_stamp = datetime.fromtimestamp(pet_stamp)
        next_stamp = pet_timer + now
        remaining = pet_stamp - now
        on_mission = await self.conf.user(ctx.author).pet.mission()
        if on_mission is False:
            await ctx.send("Sent your pet on an adventure.")
            await self.conf.user(ctx.author).pet.mission.set(True)
            await self.conf.user(ctx.author).pet_stamp.set(next_stamp.timestamp())
        elif now < pet_stamp and on_mission is True:
            await ctx.send(f"Still on a mission, wait {humanize_timedelta(timedelta=remaining)}")
        elif now > pet_stamp and on_mission is True:
            dog_responses = random.choice(doggo_responses)
            health = await self.conf.user(ctx.author).pet.hunger()
            happiness = await self.conf.user(ctx.author).pet.happy()
            health -= random.randint(10,100)
            happiness -= random.randint(10,50)
            if health <= 0 or happiness <= 0:
                await ctx.send(dog_responses + "Your pet died, rip.\n")
                return await self.conf.user(ctx.author).pet.clear()
            await self.conf.user(ctx.author).pet.hunger.set(health)
            await self.conf.user(ctx.author).pet.happy.set(happiness)
            await ctx.send(dog_responses + f"Your pet lost {health} hunger and {happiness}")
            await self.conf.user(ctx.author).pet.mission.set(False)
        
    async def feed(self, ctx):
        pass
    
    async def play(self, ctx):
        pass
    
    async def info(self, ctx):
        if await self.conf.user(ctx.author).pet.owned() is False:
            await ctx.send("Get yourself a pet first.")
        else:
            hunger = await self.conf.user(ctx.author).pet.hunger()
            name = await self.conf.user(ctx.author).pet.name()
            happiness = await self.conf.user(ctx.author).pet.happy()
            pettype = await self.conf.user(ctx.author).pet.type()
            e = discord.Embed()
            e.set_author(name=f"{ctx.author.name}'s {pettype}", icon_url=ctx.author.avatar_url)
            e.add_field(name="Pet name", value=name)
            e.add_field(name="Pet hunger", value=hunger)
            e.add_field(name="Pet happyness", value=happiness)
            e.add_field(name="Pet type", value=pettype)
            await ctx.send(embed=e)
            
    async def rename(self, ctx, name: str):
        if len(name) > 15:
            return await ctx.send("Name too long. Keep it bellow 15 chars")
        pet_owned = await self.conf.user(ctx.author).pet.owned()
        if pet_owned is True:
            await self.conf.user(ctx.author).pet.name.set(name)
            await ctx.send(f"your pet is called {name} now")
        else:
            await ctx.send("You dont have a pet")
    
