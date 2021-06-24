import discord
from redbot.core import commands
from redbot.core.utils.predicates import MessagePredicate


class Tunnel(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, msg: discord.Message):
		#if not (msg.channel.id in (779860372190396447, 830384640568066069)):
		#	return
		channel1 = 779860372190396447
		#channel2 = 830384640568066069
		channel = ctx.bot.get_channel(channel1)
		await channel.send(msg.content)