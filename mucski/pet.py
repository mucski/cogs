import discord
import random
import asyncio
from datetime import datetime, timedelta

from redbot.core import commands, checks
from .randomstuff import doggo_responses
from redbot.core.utils.chat_formatting import humanize_timedelta

class Pet:
    async def adventure(self, ctx):
        async with self.conf.user(ctx.author).pet() as pet:
            if pet:
                now = datetime.utcnow()
                timer = random.randint(20,30)
                timer = timedelta(seconds=timer)
                pet_stamp = await self.conf.user(ctx.author).pet_stamp()
                pet_stamp = datetime.fromtimestamp(pet_stamp)
                remaining = pet_stamp - now
                future = timer + now
                if pet['mission'] == False:
                    await ctx.send("Sending your pet on a mission")
                    pet['mission'] = True
                if pet_stamp > now and pet['mission'] == True:
                    await ctx.send(f"On mission {humanize_timedelta(timedelta=remaining)}")
                elif pet_stamp < now and pet['mission'] == True:
                    if pet['hunger'] <= 0 or pet['happy'] <= 0:
                        await ctx.send("Your pet died. You should take more care of it.")
                        return await self.conf.user(ctx.author).pet.clear()
                    responses = random.choice(doggo_responses)
                    pet['hunger'] -= random.randint(1,10)
                    pet['happy'] -= random.randint(1,10)
                    cookie = await self.conf.user(ctx.author).cookies()
                    earned = random.randint(100,800)
                    cookie += earned
                    await self.conf.user(ctx.author).cookies.set(cookie)
                    await ctx.send(responses.format(earned))
                    await ctx.send(f"Your pet has {pet['happy']} happynes and {pet['hunger']} hunger remaining from this adventure and gained {earned} cookies.")
                    pet['mission'] = False
                    await self.conf.user(ctx.author).pet_stamp.set(future.timestamp())
            else:
                await ctx.send("You dont own any pets")
                
    async def feed(self, ctx, item:str, amt:int):
        async with self.conf.user(ctx.author).pet() as pet:
            if pet:
                if amt == 0:
                    amt = 1
                hunger = pet['hunger']
                happy = pet['happy']
                async with self.conf.user(ctx.author).item() as item:
                    for key in item:
                        if item['type'] == 'food':
                            pet['hunger'] =+ 20
                            if amt:
                                item - amt
                            else:
                                item - 1
                        elif item['type'] == 'toy':
                            pet['happy'] =+ 20
                            if amt:
                                item - amt
                            else:
                                item - 1
                    await ctx.send(f"hunger {hunger} happyness {happy} consumed {item} {amt}")
                    
    
    async def play(self, ctx):
        pass
    
    async def info(self, ctx):
        async with self.conf.user(ctx.author).pet() as pet:
            if pet:
                hunger = pet['hunger']
                happy = pet['happy']
                pettype = pet['type']
                petname = pet['name']
                mission = pet['mission']
                e = discord.Embed(timestamp=datetime.utcnow())
                e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                e.add_field(name="Pet name", value=petname)
                e.add_field(name="Pet", value=pettype)
                e.add_field(name="On mission", value=mission)
                e.add_field(name="Hunger", value=hunger)
                e.add_field(name="Happynes", value=happy)
                await ctx.send(embed=e)
            else:
                await ctx.send("Get yourself a pet first")
                
    async def rename(self, ctx, name: str):
        async with self.conf.user(ctx.author).pet() as pet:
            if pet:
                if len(name) > 15:
                    await ctx.send("15 chars max plz")
                pet['name'] = name
                await ctx.send(f"Your pet is called {name} from now on.")
            else:
                await ctz.send("Get yourself a pet first")
    
