
from .tunnel import Tunnel

async def setup(bot):
    await bot.add_cog(Tunnel(bot))
