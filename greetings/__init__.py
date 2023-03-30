from .greetings import Greetings


async def setup(bot):
    await bot.add_cog(Greetings(bot))
