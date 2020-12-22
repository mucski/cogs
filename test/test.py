from redbot.core import commands
import random
from .words import words, words2, flags
import aiohttp
from functools import partial
import re

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
        def deEmojify(text):
            regrex_pattern = re.compile(pattern = "["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags = re.UNICODE)
            return regrex_pattern.sub(r'',text)
        await ctx.guild.get_member(ctx.author.id).edit(nick=f"{deEmojify(orig)}")
        await ctx.guild.get_member(ctx.author.id).edit(nick=f"{comp} {orig}")
        await ctx.send(f"Added {comp} to {orig}")
        #await ctx.send("You already have a flag. I'm gonna replace it.")
        #return
        #await ctx.send(orig.find(comp))
        #elif flag in flags:
            #await ctx.guild.get_member(ctx.author.id).edit(nick=f"{flags.get(flag)} {orig}")
            
    @commands.command()
    async def delflag(self, ctx):
        orig = ctx.guild.get_member(ctx.author.id).nick
        if orig is None:
            orig = ctx.guild.get_member(ctx.author.id).name
        def deEmojify(text):
            regrex_pattern = re.compile(pattern = "["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags = re.UNICODE)
            return regrex_pattern.sub(r'',text)
        
        await ctx.guild.get_member(ctx.author.id).edit(nick=f"{deEmojify(orig)}")
        await ctx.send("Done")
        
    @commands.command()
    async def flag2(self, ctx, flag):
        orig = ctx.guild.get_member(ctx.author.id).nick
        if orig is None:
            orig = ctx.guild.get_member(ctx.author.id).name
        comp = flags.get(flag)
        if comp is None:
            await ctx.send("No such flag.")
            return
        if orig.find(comp) == -1:
            orig.replace(comp,"")
            #await ctx.send("You already have a flag ..")
            return
        #await ctx.send(orig.find(comp))
        if flag in flags:
            await ctx.guild.get_member(ctx.author.id).edit(nick=f"{flags.get(flag)} {orig}")
            await ctx.send(f"Added {flags.get(flag)} to {orig}")
    
       