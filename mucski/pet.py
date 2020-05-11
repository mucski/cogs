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
            if pet["type"] == "rock":
                imgurl = "https://lh3.googleusercontent.com/proxy/ZRgffBPfbnAXUD6Pm3ui_SzB3l8Wk27O1BFr3xXCz2YXNIDXmJcWGW0mVOomB3og9y_mS7cm0o0yIbC5v5urLtfuV89jEK1GOEFCR566-uLb1oGprVo8sHI"
            if pet["type"] == "turtle":
                imgurl = "https://i.pinimg.com/originals/9a/68/38/9a6838f97b3d04b75796c59fa55c68e5.jpg"
            if pet["type"] == "cat":
                imgurl = "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcT_w1ALeih26Wp894rn7xPiJBHfRQHlei6FFenhgshqHUAIXQ0G&usqp=CAU"
            if pet["type"] == "dog":
                imgurl = "https://content3.jdmagicbox.com/comp/hyderabad/b6/040pxx40.xx40.170814152340.z1b6/catalogue/k-s-pets-services-ecil-hyderabad-dog-boardings-1knoqwn9vh.jpg?clr=4a4a1c"
            e = discord.Embed()
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
            e.set_footer(text="Dont forget to feed your pet often especially after a mission.")
            await ctx.send(embed=e)