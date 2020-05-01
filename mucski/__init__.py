from .mucski import Mucski
from .adminutils import AdminUtils

def setup(bot):
  bot.add_cog(Mucski(bot))