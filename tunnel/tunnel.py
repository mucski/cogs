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


	@commands.Cog.listener(self, msg: discord.Message):
	async def on_message(self, msg):
		#sendus
		msg = await bot.wait_for("message", check=lambda msg: msg.channel.id in (779860372190396447, 830384640568066069))
		#send the message.
		await msg.channel.send(msg.content)
