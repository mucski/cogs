import discord

from redbot.core import commands, checks

class Pet(commands.Cog):
    
    @commands.group(name="pet")
    async def pet(self, ctx):
        pass
    
    @pet.command()
    async def send(self, ctx):
        pass
    
    @pet.command()
    async def feed(self, ctx):
        pass
    
    @pet.command()
    async def play(self, ctx):
        pass
    
    @pet.command()
    async def info(self, ctx):
        if await self.conf.user(ctx.author).pet.owned() == "None":
            await ctx.send("Get yourself a pet first.")
        else:
            health = await self.conf.user(ctx.author).pet.health()
            name = await self.conf.user(ctx.author).pet.name()
            happiness = await self.conf.user(ctx.author).pet.happiness()
            pettype = await self.conf.user(ctx.author).pet.type()
            e = discord.Embed()
            e.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            e.add_field(name="Pet health", value=health)
            e.add_field(name="Pet name", value=name)
            e.add_field(name="Pet happynes", value=happiness)
            e.add_field(name="Pet type", value=pettype)
            await ctx.send(embed=e)
    
