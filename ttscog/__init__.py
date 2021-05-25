from .ttscog import TTSCog

async def setup(bot):
    bot.add_cog(TTSCog(bot))
