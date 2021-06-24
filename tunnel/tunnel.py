import discord
from redbot.core import commands
from redbot.core.utils.predicates import MessagePredicate


class Tunnel(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def tunnel(self, ctx):
		msg = await ctx.bot.wait_for("message", check=lambda msg: msg.channel.id in (779860372190396447, 830384640568066069))
		await msg.channel.send(msg.content)
		