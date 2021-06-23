from redbot.core import commands


class Tunnel(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def tunnel(self, ctx, *, msg):
		channel = self.bot.get_channel(779860372190396447)
		await channel.send(msg)
