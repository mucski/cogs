from .hirez import HiRez


async def setup(bot):
    await bot.add_cog(HiRez(bot))
