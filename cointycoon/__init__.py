from .cointycoon import CoinTycoon

def setup(bot):
    bot.add_cog(CoinTycoon(bot))