from .snapchatchan import SnapChatChan


async def setup(bot):
    await bot.add_cog(SnapChatChan(bot))