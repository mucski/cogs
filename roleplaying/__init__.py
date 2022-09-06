from .roleplaying import Roleplaying


async def setup(bot):
    await bot.add_cog(Roleplaying(bot))
