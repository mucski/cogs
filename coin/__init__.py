from .coin import Coin


async def setup(bot):
    await bot.add_cog(Coin(bot))
