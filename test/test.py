from redbot.core import commands
import random
from .words import words, words2, flags
import aiohttp
from PIL import Image, ImageDraw
from functools import partial

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def whoami(self, ctx):
        word = random.choice(words)
        word2 = random.choice(words2)
        await ctx.send(f"{word} {word2}")
        
    @commands.command()
    async def flag(self, ctx, flag):
        orig = ctx.guild.get_member(ctx.author.id).nick
        if orig is None:
            orig = ctx.guild.get_member(ctx.author.id).name
        comp = flags.get(flag)
        if comp is None:
            await ctx.send("No such flag.")
            return
        if orig.find(comp,1) != -1:
            await ctx.send("You already have a flag ..")
            return
        await ctx.send(comp)
        #if flag in flags:
            #await ctx.guild.get_member(ctx.author.id).edit(nick=f"{flags.get(flag)} {orig}")
            #await ctx.send(f"Added {flags.get(flag)} to {orig}")
    
       