import discord
from redbot.core import commands
from .randomstuff import kisslist, slaplist, punchlist, cuddlelist, sadlist, patlist, huglist, licklist, bitelist, middlefingerlist
from .randomstuff import twerklist, dancelist, crylist, meowlist, rawrlist, angrylist, shylist, blushlist, killlist, karatelist
from .randomstuff import rektlist, hungrylist, thirstylist, happylist, greetlist, wavelist, hornylist, marrylist, praylist, curselist, smokelist
from .randomstuff import lewdlist, sleepylist, lazylist, thinklist, richlist, poorlist, nomlist, pokelist, booplist, highfivelist
from .randomstuff import ticklelist, bullylist, toxiclist, trashlist, popcornlist, lovelist, spanklist
import random


class Roleplaying(commands.Cog):
	"""Simple roleplaying cog by mucski"""
	def __init__(self, bot):
		self.bot = bot
		
		
	@classmethod
	async def img_grab(self, cmd, action, author, member):
		e = discord.Embed()
		img = random.choice(cmd)
		e.set_image(url=img)
		if member:
			member = member.mention
		else:
			member = ""
		e.description=f"{author.mention} {action} {member}"
		return e

	@commands.command()
	async def kiss(self, ctx, member: discord.Member = None):
		author = ctx.author
		if member:
		    if member.id == 855197640153104424:
		        member = None
		        embed = await self.img_grab(kisslist, "kisses **Mucski**'s ass", author, member)
		        await ctx.send(embed=embed)
		        return
		embed = await self.img_grab(kisslist, "kisses", author, member)
		await ctx.send(embed=embed)

	@commands.command()
	async def punch(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(punchlist, "punches", author, member)
		await ctx.send(embed=embed)

	@commands.command()
	async def cuddle(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(cuddlelist, "cuddles", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def hug(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(huglist, "hugs", author, member)
		await ctx.send(embed=embed)

	@commands.command()
	async def pat(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(patlist, "pats", author, member)
		await ctx.send(embed=embed)

	@commands.command()
	async def slap(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(slaplist, "slaps", author, member)
		await ctx.send(embed=embed)

	@commands.command()
	async def sad(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(sadlist, "is sad", author, member)
		await ctx.send(embed=embed)

	@commands.command()
	async def lick(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(licklist, "licks", author, member)
		await ctx.send(embed=embed)

	@commands.command()
	async def bite(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(bitelist, "bites", author, member)
		await ctx.send(embed=embed)

	@commands.command()
	async def middlefinger(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(middlefingerlist, "flips off", author, member)
		await ctx.send(embed=embed)

	@commands.command()
	async def twerk(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(twerklist, "twerks on", author, member)
		await ctx.send(embed=embed)

	@commands.command()
	async def dance(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(dancelist, "dances with", author, member)
		await ctx.send(embed=embed)

	@commands.command()
	async def cry(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(crylist, "cries", author, member)
		await ctx.send(embed=embed)

	@commands.command()
	async def meow(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(meowlist, "meows", author, member)
		await ctx.send(embed=embed)

	@commands.command()
	async def rawr(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(rawrlist, "rawrs", author, member)
		await ctx.send(embed=embed)

	@commands.command()
	async def angry(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(angrylist, "is angry", author, member)
		await ctx.send(embed=embed)

	@commands.command()
	async def shy(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(shylist, "is shy", author, member)
		await ctx.send(embed=embed)

	@commands.command()
	async def blush(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(blushlist, "blushes", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def kill(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(killlist, "kills", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def karate(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(karatelist, "kicks", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def rekt(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(rektlist, "reks", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def hungry(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(hungrylist, "is hungry", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def thirsty(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(thirstylist, "is thirsty", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def happy(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(happylist, "is happy", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def greet(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(greetlist, "greets", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def wave(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(wavelist, "waves to", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def horny(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(hornylist, "is horny", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def marry(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(marrylist, "marries", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def pray(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(praylist, "prays", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def curse(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(curselist, "curses", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def smoke(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(smokelist, "smokes", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def lewd(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(lewdlist, "is lewd", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def sleepy(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(sleepylist, "is sleepy", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def lazy(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(lazylist, "is lazy", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def think(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(thinklist, "is thinking", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def rich(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(richlist, "is rich", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def poor(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(poorlist, "is poor", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def nom(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(nomlist, "noms on", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def poke(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(pokelist, "pokes", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def boop(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(booplist, "boops", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def highfive(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(highfivelist, "high fives", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def tickle(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(ticklelist, "tickles", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def bully(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(bullylist, "bullies", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def toxic(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(toxiclist, "is toxic", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def trash(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(trashlist, "trashes", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def popcorn(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(popcornlist, "is eating popcorn", author, member)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def love(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(lovelist, "loves", author, member)
		await ctx.send(embed=embed)

	@commands.command()
	async def spank(self, ctx, member: discord.Member = None):
		author = ctx.author
		embed = await self.img_grab(spanklist, "spanks", author, member)
		await ctx.send(embed=embed)
