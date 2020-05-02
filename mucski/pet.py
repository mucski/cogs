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
        pass
    
