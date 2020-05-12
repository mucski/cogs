import discord
import asyncio
from redbot.core import commands, checks
from datetime import datetime, timedelta
from .randomstuff import petlist
from .taskhelper import TaskHelper

class Pet(TaskHelper, commands.Cog):
    def __init__(self):
        TaskHelper.__init__(self)
        self.bot.loop.create_task(self._worker())
        
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
        coins -= price
        if coins <= 0:
            await ctx.send("Not enough coins to buy that pet.")
            return
        async with self.conf.user(ctx.author).pets() as pet:
            pet["name"] = name.capitalize()
            pet["mission"] = False
            pet["hunger"] = 100
            pet["happy"] = 100
            pet["clean"] = 100
            pet["type"] = name.lower()
            await self.conf.user(ctx.author).coins.set(coins)
            await ctx.send(f"You bought a {pet['type']} and spent {price} coins, take good care of it. See [p]pet info for stats and other stuff.")
        
    @pet.command()
    async def info(self, ctx):
        if not await self.conf.user(ctx.author).pets():
            await ctx.send("You dont own any pets.")
            return
        async with self.conf.user(ctx.author).pets() as pet:
            if pet["type"] == "rock":
                imgurl = "https://lh3.googleusercontent.com/proxy/ZRgffBPfbnAXUD6Pm3ui_SzB3l8Wk27O1BFr3xXCz2YXNIDXmJcWGW0mVOomB3og9y_mS7cm0o0yIbC5v5urLtfuV89jEK1GOEFCR566-uLb1oGprVo8sHI"
            if pet["type"] == "turtle":
                imgurl = "https://i.pinimg.com/originals/9a/68/38/9a6838f97b3d04b75796c59fa55c68e5.jpg"
            if pet["type"] == "cat":
                imgurl = "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcT_w1ALeih26Wp894rn7xPiJBHfRQHlei6FFenhgshqHUAIXQ0G&usqp=CAU"
            if pet["type"] == "dog":
                imgurl = "https://content3.jdmagicbox.com/comp/hyderabad/b6/040pxx40.xx40.170814152340.z1b6/catalogue/k-s-pets-services-ecil-hyderabad-dog-boardings-1knoqwn9vh.jpg?clr=4a4a1c"
            e = discord.Embed(color=await self.bot.get_embed_color(ctx))
            e.set_author(name=f"{ctx.author.name}'s {pet['type']}", icon_url=imgurl)
            e.set_thumbnail(url=imgurl)
            e.add_field(name="Name", value=pet["name"])
            e.add_field(name="Type", value=pet["type"])
            e.add_field(name="Hunger", value=pet["hunger"])
            e.add_field(name="Happy", value=pet["happy"])
            e.add_field(name="Clean", value=pet["clean"])
            if pet["mission"] == True:
                e.add_field(name="On Mission", value="Yes, remaining:")
            else:
                e.add_field(name="On Mission", value="Nope")
            e.set_footer(text="Dont forget to feed your pet often "
                                "especially after a mission.")
            await ctx.send(embed=e)
            
    @pet.command()
    async def rename(self, ctx, *, name):
        if not await self.conf.user(ctx.author).pets():
            await ctx.send("You dont own any pets")
            return
        if len(name) > 23:
            await ctx.send("Lets not, okay? Try a shorter name (23 chars max)")
            return
        async with self.conf.user(ctx.author).pets() as pet:
            pet['name'] = name
            await ctx.send(f"Your pet is now called {name}")
            
    @pet.command()
    async def send(self, ctx):
        if not await self.conf.user(ctx.author).pets():
            await ctx.send("You dont have any pets")
            return
        channel = ctx.channel
        await self.conf.user(ctx.author).channel.set(channel.id)
        petStamp = await self.conf.user(ctx.author).p_stamp()
        if petStamp:
            await ctx.send("Your pet is already in a mission,"
                            "wait for it to finish.")
            return
        now = datetime.utcnow()
        timer = timedelta(seconds=30)
        future = timer + now
        future = future.timestamp()
        await self.conf.user(ctx.author).p_stamp.set(future)
        async with self.conf.user(ctx.author).pets() as pet:
            pet["mission"] = True
        tempStamp = datetime.fromtimestamp(future)
        remaining = tempStamp - now
        remaining = remaining.seconds
        user = ctx.author
        await ctx.send("Sent pet on a mission.")
        await self._timer(remaining, channel, user)
        
    async def _timer(self, remaining, channel, user):
        await asyncio.sleep(remaining)
        await self._stop(channel, user)
        
    async def _worker(self):
        await self.bot.wait_until_ready()
        now = datetime.utcnow()
        users = await self.conf.all_users()
        for user_id, user_data in users.items():
            user = self.bot.get_user(user_id)
            if not user:
                continue
            channel = self.bot.get_channel(user_data['channel'])
            if not channel:
                continue
            stamp = datetime.fromtimestamp(user_data['p_stamp'])
            if stamp > now:
                await self._stop(channel, user)
            else:
                remaining = stamp - now
                remaining = remaining.seconds
                self.schedule_task(self._timer(remaining, channel, user))
    
    async def _stop(self, channel, user):
        await self.conf.user(user).pets.set_raw("mission", value=False)
        await self.conf.user(user).p_stamp.clear()
        type = await self.conf.user(user).pets.get_raw("type")
        await channel.send(f"Yo {user.mention} your {type} returned")