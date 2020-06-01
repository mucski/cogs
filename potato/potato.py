import discord
from redbot.core import commands, Config

class Potato(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Config.get_conf(self, 8272727485, force_registration=True)
        
        default_user = {
            "data": {} # {potato: 0, and more}
        }
        default_guild = {
            "guild_data": {} # {channel: and more}
        }
        self.db.register_user(**default_user)
        self.db.register_guild(**default_guild)
        
    @commands.group(aliases=['p'], invoke_without_command=True)
    async def potato(self, ctx):
        async with self.db.user(ctx.author).data() as data:
            if data is None:
                await ctx.send("Start playing first by using one of the action commands (farm, daily)")
                return
            embed=discord.Embed(color=await self.bot.get_embed_color(ctx), title="🥔 potatos owned 🥔")
            embed.description(f"{ctx.author.name} has {potato} 🥔 potatoes 🥔 in his pocket and {silo} 🥔 potatoes 🥔 stashed in silo, jelly yet?")
            await ctx.send(embed=embed)
    
    @potato.command()
    async def give(self, ctx):
        pass
    
    @potato.command()
    async def inspect(self, ctx):
        pass
    
    @potato.command()
    async def steal(self, ctx):
        pass
    
    @potato.command()
    async def farm(self, ctx):
        pass
    
    @potato.command()
    async def gamble(self, ctx):
        pass