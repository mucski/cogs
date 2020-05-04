import discord
import random
import asyncio
from datetime import datetime, timedelta

from redbot.core import commands, checks
from .randomstuff import doggo_responses
from redbot.core.utils.chat_formatting import humanize_timedelta

class Pet:
    async def adventure(self, ctx):
        owned = await self.conf.user(ctx.author).pet()
        if owned is None:
            return await ctx.send("No pet no gain")
        now = datetime.utcnow().replace(microsecond=0)
        time = random.randint(100,500)
        pet_timer = timedelta(seconds=time)
        pet_stamp = await self.conf.user(ctx.author).pet_stamp()
        pet_stamp = datetime.fromtimestamp(pet_stamp)
        next_stamp = pet_timer + now
        remaining = pet_stamp - now
        async with self.conf.user(ctx.author).pet() as pet:
            if pet['mission'] == False:
                await ctx.send("Sent pet on adventure")
                pet['mission'] = True
                await self.conf.user(ctx.author).pet_stamp.set(next_stamp.timestamp())
            if now < pet_stamp:
                await ctx.send(f"Still on a mission, wait {humanize_timedelta(timedelta=remaining)}")
            elif now > pet_stamp and pet['mission'] == True:
                hunger = pet['hunger']
                hunger -= max(random.randint(1,10),0)
                happy = pet['happy']
                happy -= max(random.randint(1,10),0)
                cookie = await self.conf.user(ctx.author).cookies()
                value = random.randint(300,700)
                earned = cookie + value
                pet['mission'] = False
                if hunger == 0 or happy == 0:
                    dog_responses = random.choice(doggo_responses)
                    await ctx.send(dog_responses.format(value) + "\nYour pet died, rip.")
                    return await self.conf.user(ctx.author).pet.clear()
            await ctx.send(dog_responses.format(value) + f"\nYour pet lost {hunger} hunger and {happy} happyness")
        
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
                petstats = await self.conf.user(ctx.author).pet()
            except KeyError:
                await ctx.send("no such pet")
            await ctx.send(petstats)
            await ctx.send(petstats['name'])
            
    async def rename(self, ctx, name: str):
        if len(name) > 15:
            return await ctx.send("Name too long. Keep it bellow 15 chars")
        pet_owned = await self.conf.user(ctx.author).pet.owned()
        if pet_owned is True:
            await self.conf.user(ctx.author).pet.name.set(name)
            await ctx.send(f"your pet is called {name} now")
        else:
            await ctx.send("You dont have a pet")
    
