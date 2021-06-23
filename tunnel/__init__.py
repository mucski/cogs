
from .tunnel import Tunnel

async def setup(bot):
    bot.add_cog(Tunnel(bot))
