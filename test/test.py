from redbot.core import commands, checks, Config

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tree.context_menu(name='say')
    async def say(interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message('I said something!')
