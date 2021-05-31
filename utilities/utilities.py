from redbot.core import commands, checks
from redbot.core.utils.chat_formatting import text_to_file
import random
from .words import words, words2, flags
from .country import country
import re
import subprocess
import discord


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("info")

    @commands.command()
    async def whoami(self, ctx):
        word = random.choice(words)
        word2 = random.choice(words2)
        await ctx.send(f"{word} {word2}")

    @commands.command()
    async def flag(self, ctx, *, flag):
        orig = ctx.guild.get_member(ctx.author.id).nick
        if orig is None:
            orig = ctx.guild.get_member(ctx.author.id).name
        if len(flag) < 3:
            if flag == "uk":
                comp = flags.get("gb")
            else:
                comp = flags.get(flag.lower())
        else:
            comp2 = country.get(flag.lower())
            comp = flags.get(comp2)
        if not comp:
            await ctx.send("No such flag buddy.")
            return
        def deEmojify(text):
            regrex_pattern = re.compile(
                pattern="["
                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                        "]+", flags=re.UNICODE)
            return regrex_pattern.sub(r'', text)
        # newnick = deEmojify(orig)
        try:
            await ctx.guild.get_member(ctx.author.id).edit(nick=f"{comp} {orig.strip()}")
        except (discord.errors.Forbidden, discord.errors.HTTPException):
            await ctx.send("Missing permissions or nickname too large (32 chars max)")
            return
        await ctx.send(f"Added {comp} to {orig.strip()}'s nickname. To remove it use delflag command.")

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
        except (discord.errors.Forbidden, discord.errors.HTTPException):
            await ctx.send("Missing permissions.")
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
        
    @commands.command()
    async def say(self, ctx, *, stuff):
        async for log in ctx.channel.history(limit=1):
            if log.author == ctx.author:
                await log.delete()
        await ctx.send(stuff)
        
    @commands.command()
    async def info(self, ctx):
        desc = (
            "Multipurpose bot hosted by mucski, created by Twentysix\n"
            "For support you can contact my owner with the contact command\n"
            "Or join our discord server: https://discord.gg/qt2tXUrH"
        )
        e = discord.Embed(title=f"{self.bot.user.display_name}'s info", color=await self.bot.get_embed_color(ctx), description=desc)
        await ctx.send(embed=e)
        
    def cog_unload(self):
        self.bot.add_command("info")