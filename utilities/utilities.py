from redbot.core import commands, checks
from redbot.core.utils.chat_formatting import text_to_file
import random
from .words import words, words2, flags, country
import re
import subprocess
import discord


class Utilities(commands.Cog):
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
        if len(flag) < 2:
            comp = flags.get(flag.lower())
        else:
            country = country.get(flag.lower())
            comp = flags.get(country)
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
        try:
            await ctx.guild.get_member(ctx.author.id).edit(nick=f"{comp} {newnick.strip()}")
        except discord.errors.Forbidden:
            await ctx.send("Missing permssion: Change users nickname")
            return
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
        try:
            await ctx.guild.get_member(ctx.author.id).edit(nick=f"{deEmojify(orig)}")
        except discord.errors.Forbidden:
            await ctx.send("Missing permission: Change users nickname")
            return
        await ctx.send("Done")
        
    @commands.command()
    @checks.is_owner()
    async def console(self, ctx, *, cmd):
    # The recommended way in Python 3.5 and above is to use subprocess.
        output = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, shell=True, stderr=subprocess.STDOUT)
        #subprocess = subprocess.Popen(shell = True, stdout = subprocess.PIPE)
        #output = subprocess.stdout.read()
        response = output.stdout
        if len(response) > 2000:
            try:
                file = text_to_file(response, "console.txt")
                await ctx.send(file=file)
            except discord.errors.HTTPException:
                await ctx.send("File too large.")
                return
        else:
            await ctx.send("```\n" + response + "\n```")

    @commands.command(aliases=["emoji"])
    async def emote(self, ctx, emoji: discord.PartialEmoji):
        await ctx.send(emoji.url)

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        await ctx.send(member.avatar_url)
