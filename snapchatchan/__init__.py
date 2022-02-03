from .snapchatchan import SnapChatChan


def setup(bot):
    bot.add_cog(SnapChatChan(bot))