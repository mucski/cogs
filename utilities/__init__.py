from .utilities import Utilities

async def setup(bot):
    bot.add_cog(Utilities(bot))
