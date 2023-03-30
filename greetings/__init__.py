from .greetings import Greetings


async def setup(bot):
    bot.add_cog(Greetings(bot))
