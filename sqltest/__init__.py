from .sqltest import Sqltest

def setup(bot):
    bot.add_cog(Sqltest(bot))