from .mucski import Mucski

def setup(bot):
  bot.add_cog(Mucski(bot))
  bot.add_cog(AdminUtils(bot))