import discord
from redbot.core import commands


class Tunnel(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, msg: discord.Message):
	    # gabys server channel
		channel1 = 857721514006413363
		# paladins with a pint channel
		channel2 = 856512859919745034
		if msg.author == self.bot.user:
			return
		if not (msg.channel.id in (channel1, channel2)):
			return
		if msg.channel.id == channel1:
			channel = self.bot.get_channel(channel2)
			await channel.send(f"**{msg.author}**: {msg.content}")
		if msg.channel.id == channel2:
			channel = self.bot.get_channel(channel1)
			await channel.send(f"**{msg.author}**: {msg.content}")