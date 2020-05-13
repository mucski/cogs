from .giveaway import GiveAway

def setup(bot):
    bot.add_cog(GiveAway(bot))
