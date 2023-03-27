from .utilities import Utilities

async def setup(bot):
    # bot.tree.add_command(say)
    await bot.add_cog(Utilities(bot))
