from .coin import Coin


def setup(bot):
    bot.add_cog(Coin(bot))
