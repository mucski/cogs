
# import discord
from redbot.core import commands


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = bot.get_channel()  # the channel ID
        await channel.send(f"Welcome {member.mention}")