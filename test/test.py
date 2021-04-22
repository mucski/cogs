from redbot.core import commands
import random
from .words import words, words2, flags
# import aiohttp
# from functools import partial
import re
import subprocess


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
        comp = flags.get(flag.lower())
        if comp is None:
            await ctx.send("No such flag.")
            return

        def deEmojify(text):
            regrex_pattern = re.compile(
                pattern="["
                        # u"\U0001F600-\U0001F64F"  # emoticons
                        # u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                        # u"\U0001F680-\U0001F6FF"  # transport & map symbols
                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                        "]+", flags=re.UNICODE)
            return regrex_pattern.sub(r'', text)
        newnick = deEmojify(orig)
        # await ctx.guild.get_member(
        # ctx.author.id).edit(nick=f"{deEmojify(orig)}")
        await ctx.guild.get_member(ctx.author.id).edit(nick=f"{comp} "
                                                       f"{newnick.strip()}")
        await ctx.send(f"Changed {newnick.strip()}'s country to {comp}")
        # await ctx.send("You already have a flag. I'm gonna replace it.")
        # return
        # await ctx.send(orig.find(comp))
        # elif flag in flags:
        #   await ctx.guild.get_member(
        # ctx.author.id).edit(nick=f"{flags.get(flag)} {orig}")

    @commands.command()
    async def delflag(self, ctx):
        orig = ctx.guild.get_member(ctx.author.id).nick
        if orig is None:
            orig = ctx.guild.get_member(ctx.author.id).name

        def deEmojify(text):
            regrex_pattern = re.compile(
                pattern="["
                        # u"\U0001F600-\U0001F64F"  # emoticons
                        # u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                        # u"\U0001F680-\U0001F6FF"  # transport & map symbols
                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                        "]+", flags=re.UNICODE)
            return regrex_pattern.sub(r'', text)

        await ctx.guild.get_member(ctx.author.id).edit(
            nick=f"{deEmojify(orig)}")
        await ctx.send("Done")
        
    @commands.command()
    async def console(self, ctx, cmd):
    # The recommended way in Python 3.5 and above is to use subprocess.
        output = subprocess.run(cmd, capture_output=True).stdout
        #subprocess = subprocess.Popen(shell = True, stdout = subprocess.PIPE)
        #output = subprocess.stdout.read()
        await ctx.send(output)