from .sfx import SFX

async def setup(bot):
    bot.add_cog(SFX(bot))
