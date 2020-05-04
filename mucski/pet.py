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
            pet_hunger = await self.conf.user(ctx.author).pet.hunger()
            pet_happy = await self.conf.user(ctx.author).pet.happy()
            hunger = random.randint(1,10)
            happy = random.randint(1,10)
            final_hunger -= hunger
            final_happy -= happy
            cookie = await self.conf.user(ctx.author).cookies()
            value = random.randint(300,700)
            earned = cookie + value
            if final_hunger <= 0 or final_happy <= 0:
                await ctx.send(dog_responses.format(value) + "\nYour pet died, rip.")
                return await self.conf.user(ctx.author).pet.clear()
            await self.conf.user(ctx.author).pet.hunger.set(final_hungry)
            await self.conf.user(ctx.author).pet.happy.set(final_happy)
            await ctx.send(dog_responses.format(value) + f"\nYour pet lost {hunger} hunger and {happy} happyness")
            await self.conf.user(ctx.author).pet.mission.set(False)
        
    async def feed(self, ctx, item:str, amt:int):
        if amt <= 0:
            amt = 1
        inventory = await self.conf.user(ctx.author).pet.item.food()
        quantity = await self.conf.user(ctx.author).pet.item.food.quantity()
    
    async def play(self, ctx):
        pass
    
    async def info(self, ctx):
        if await self.conf.user(ctx.author).pet.owned() is False:
            await ctx.send("Get yourself a pet first.")
        else:
            try:
                petstats = await self.conf.user(ctx.author).get_raw(pet)
            except KeyError:
                await ctx.send("no such pet")
            e = discord.Embed()
            e.set_author(name=f"{ctx.author.name}'s", icon_url=ctx.author.avatar_url)
            e.add_field(name="Pet name", value=petstats['name'])
            e.add_field(name="Pet hunger", value=petstats['hunger'])
            e.add_field(name="Pet happyness", value=petstats['hungry']
            e.add_field(name="Pet type", value=petstats['type'])
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
    
