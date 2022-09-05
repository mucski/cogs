from redbot.core import commands, checks, Config

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_commands.command(name="test", description=_("List all playlists you have access to on the invoked context"))
    @app_commands.guild_only()
    async def slash_commands_test(self, interaction: InteractionT):
        await ctx.send("hello world")
