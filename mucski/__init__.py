from .mucski import Mucski
from .mucski import AdminUtils

def setup(bot):
  bot.add_cog(Mucski(bot))
  bot.add_cog(AdminUtils(bot))