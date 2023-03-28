from .slashtest import SlashTest, repeat, hi


async def setup(bot):
    bot.tree.add_command(repeat)
    bot.tree.add_command(hi)
    await bot.add_cog(SlashTest(bot))