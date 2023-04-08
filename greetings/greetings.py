
# import discord
from redbot.core import commands


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 939484898773827614:
            channel = self.bot.get_channel(971361677348044862)  # the channel ID
            await channel.send(f"Welcome to Mystic Valley {member.mention}, enjoy your stay. Please do read the rules in {self.bot.get_channel(971361336594403368).mention}")