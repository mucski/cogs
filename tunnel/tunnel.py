from redbot.core import commands, checks
import discord


#start of awesome script

class Tunnel(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command()
	async def tunnel(self, ctx, *, message):
		channel = self.bot.get_channel(779860372190396447)
		await channel.send(f"{ctx.author} sent {message}")


	@commands.Cog.listener()
	async def on_message(self, msg):
	    channel1 = 779860372190396447
	    channel2 = 830384640568066069

	    msg = await bot.wait_for("message", check=lambda msg: msg.channel.id in (channel1, channel2))

		await msg.channel.send(msg.content)
