import discord
from redbot.core import commands
from .randomstuff import kisslist, slaplist, punchlist, cuddlelist, sadlist, patlist, huglist, licklist, bitelist, middlefingerlist, twerklist, dancelist, crylist, meowlist, rawrlist, angrylist, shylist, blushlist
import random


class Roleplaying(commands.Cog):
	"""Simple roleplaying cog by mucski"""
	def __init__(self, bot):
		self.bot = bot

	@classmethod
	async def img_grab(self, cmd, action, author, member):
		img = random.choice(cmd)
		e = discord.Embed()
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
