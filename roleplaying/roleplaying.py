import random
from typing import Optional, List

import discord
from redbot.core import commands

from .randomstuff import (
    kisslist, slaplist, punchlist, cuddlelist, sadlist, patlist, huglist, licklist, bitelist,
    middlefingerlist, twerklist, dancelist, crylist, meowlist, rawrlist, angrylist, shylist,
    blushlist, killlist, karatelist, rektlist, hungrylist, thirstylist, happylist, greetlist,
    wavelist, hornylist, marrylist, praylist, curselist, smokelist, lewdlist, sleepylist,
    lazylist, thinklist, richlist, poorlist, nomlist, pokelist, booplist, highfivelist,
    ticklelist, bullylist, toxiclist, trashlist, popcornlist, lovelist, spanklist,
)


class Roleplaying(commands.Cog):
    """
    Simple roleplaying cog by Mucski.
    """
    def __init__(self, bot):
        self.bot = bot

    def img_grab(
        self,
        options: List[str],
        action_self: str,
        action_targetted: str,
        author: discord.Member,
        member: Optional[discord.Member],
    ):
        if member is None:
            description = f"{author.mention} {action_self}"
        else:
            description = f"{author.mention} {action_targetted} {member.mention}"
        e = discord.Embed(description=description)
        img = random.choice(options)
        e.set_image(url=img)
        return e
    
    @commands.hybrid_group()
    async def rp(self, ctx):
        """Roleplaying slash commands"""
        pass

    @rp.command()
    async def kiss(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(kisslist, "sends kisses", "kisses", ctx.author, member))

    @rp.command()
    async def punch(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(punchlist, "punches", "punches", ctx.author, member))

    @rp.command()
    async def cuddle(self, ctx, member: discord.Member = None):
        await ctx.send(
            embed=self.img_grab(cuddlelist, "cuddles", "cuddles with", ctx.author, member)
        )

    @rp.command()
    async def hug(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(huglist, "wants to hug", "hugs", ctx.author, member))

    @rp.command()
    async def pat(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(patlist, "sends pats", "pats", ctx.author, member))

    @rp.command()
    async def slap(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(slaplist, "slaps", "slaps", ctx.author, member))

    @rp.command()
    async def sad(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(sadlist, "is sad", "is sad at", ctx.author, member))

    @rp.command()
    async def lick(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(licklist, "licks", "licks", ctx.author, member))

    @rp.command()
    async def bite(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(bitelist, "bites", "bites", ctx.author, member))

    @rp.command()
    async def middlefinger(self, ctx, member: discord.Member = None):
        await ctx.send(
            embed=self.img_grab(
                middlefingerlist, "flips off everyone", "flips off", ctx.author, member
            )
        )

    @rp.command()
    async def twerk(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(twerklist, "twerks", "twerks on", ctx.author, member))

    @rp.command()
    async def dance(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(dancelist, "dances", "dances with", ctx.author, member))

    @rp.command()
    async def cry(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(crylist, "cries", "cries", ctx.author, member))

    @rp.command()
    async def meow(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(meowlist, "meows", "meows at", ctx.author, member))

    @rp.command()
    async def rawr(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(rawrlist, "rawrs", "rawrs towards", ctx.author, member))

    @rp.command()
    async def angry(self, ctx, member: discord.Member = None):
        await ctx.send(
            embed=self.img_grab(angrylist, "is angry", "is angry at", ctx.author, member)
        )

    @rp.command()
    async def shy(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(shylist, "is shy", "is shy at", ctx.author, member))

    @rp.command()
    async def blush(self, ctx, member: discord.Member = None):
        await ctx.send(
            embed=self.img_grab(blushlist, "blushes", "blushes because of", ctx.author, member)
        )

    @commands.command()
    async def kill(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(killlist, "kills", "kills", ctx.author, member))

    @commands.command()
    async def karate(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(karatelist, "kicks", "kicks", ctx.author, member))

    @commands.command()
    async def rekt(self, ctx, member: discord.Member = None):
        await ctx.send(
            embed=self.img_grab(rektlist, "says: Get rekt!", "rekts", ctx.author, member)
        )

    @rp.command()
    async def hungry(self, ctx, member: discord.Member = None):
        await ctx.send(
            embed=self.img_grab(hungrylist, "is hungry", "is hungry for", ctx.author, member)
        )

    @rp.command()
    async def thirsty(self, ctx, member: discord.Member = None):
        await ctx.send(
            embed=self.img_grab(thirstylist, "is thirsty", "is thirsty for", ctx.author, member)
        )

    @rp.command()
    async def happy(self, ctx, member: discord.Member = None):
        await ctx.send(
            embed=self.img_grab(happylist, "is happy", "is happy for", ctx.author, member)
        )

    @rp.command()
    async def greet(self, ctx, member: discord.Member = None):
        await ctx.send(
            embed=self.img_grab(greetlist, "greets everyone 👋", "greets", ctx.author, member)
        )

    @rp.command()
    async def wave(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(wavelist, "waves", "waves at", ctx.author, member))

    @rp.command()
    @rp.is_nsfw()
    async def horny(self, ctx, member: discord.Member = None):
        await ctx.send(
            embed=self.img_grab(hornylist, "is horny", "is horny for", ctx.author, member)
        )

    @rp.command()
    async def marry(self, ctx, member: discord.Member = None):
        await ctx.send(
            embed=self.img_grab(marrylist, "wants to marry", "marries", ctx.author, member)
        )

    @rp.command()
    async def pray(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(praylist, "prays", "prays to", ctx.author, member))

    @rp.command()
    async def curse(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(curselist, "curses", "curses at", ctx.author, member))

    @rp.command()
    async def smoke(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(smokelist, "smokes", "smokes with", ctx.author, member))

    @rp.command()
    @rp.is_nsfw()
    async def lewd(self, ctx, member: discord.Member = None):
        await ctx.send(
            embed=self.img_grab(lewdlist, "feels lewd", "feels lewd towards", ctx.author, member)
        )

    @rp.command(aliases=["tired"])
    async def sleepy(self, ctx, member: discord.Member = None):
        await ctx.send(
            embed=self.img_grab(sleepylist, "is sleepy", "wants to sleep with", ctx.author, member)
        )

    @rp.command()
    async def lazy(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(lazylist, "is lazy", "is lazy", ctx.author, member))

    @rp.command()
    async def think(self, ctx, member: discord.Member = None):
        await ctx.send(
            embed=self.img_grab(thinklist, "is thinking", "is thinking with", ctx.author, member)
        )

    @rp.command()
    async def rich(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(richlist, "is rich", "is rich", ctx.author, member))

    @rp.command()
    async def poor(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(poorlist, "is poor", "is poor", ctx.author, member))

    @rp.command()
    async def nom(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(nomlist, "noms", "noms on", ctx.author, member))

    @rp.command()
    async def poke(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(pokelist, "pokes", "pokes", ctx.author, member))

    @rp.command()
    async def boop(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(booplist, "boops", "boops", ctx.author, member))

    @rp.command()
    async def highfive(self, ctx, member: discord.Member = None):
        await ctx.send(
            embed=self.img_grab(highfivelist, "high fives", "high fives", ctx.author, member)
        )

    @rp.command()
    async def tickle(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(ticklelist, "tickles", "tickles", ctx.author, member))

    @rp.command()
    async def bully(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(bullylist, "is a bully", "bullies", ctx.author, member))

    @rp.command()
    async def toxic(self, ctx, member: discord.Member = None):
        await ctx.send(
            embed=self.img_grab(toxiclist, "is toxic", "is toxic towards", ctx.author, member)
        )

    @rp.command()
    async def trash(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(trashlist, "trashes", "trashes", ctx.author, member))

    @rp.command()
    async def popcorn(self, ctx, member: discord.Member = None):
        await ctx.send(
            embed=self.img_grab(
                popcornlist, "is eating popcorn", "is eating popcorn with", ctx.author, member
            )
        )

    @rp.command()
    async def love(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(lovelist, "loves", "loves", ctx.author, member))

    @rp.command()
    @commands.is_nsfw()
    async def spank(self, ctx, member: discord.Member = None):
        await ctx.send(embed=self.img_grab(spanklist, "spanks", "spanks", ctx.author, member))
