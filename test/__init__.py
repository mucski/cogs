from .test import Test


# Needed for future cogs
async def setup(bot):
    await bot.add_cog(Test(bot))