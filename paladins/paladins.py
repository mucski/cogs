import aiohttp
import discord
import asyncio
import re
from redbot.core import commands, Config
from redbot.core.utils.predicates import MessagePredicate

class Paladins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #thanks DevilXD
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        asyncio.create_task(self.session.close())
          
    # shit rewrite
    @commands.command()
    async def last(self, ctx, player, platform="pc"):
        """If you have a name with space in it please use a double quote like so "john doe" """
        async with self.session.get(f"https://nonsocial.herokuapp.com/api/lastmatch?player={player}&platform={platform}") as r:
            text = await r.text()
            text = text.replace('-', '|').replace('Match', '|')
            text = re.sub('[()]', '', text)
            text = text.split('| ')
            test = len(text)
            newlist = []
            for i in range(test):
                newlist.append(text[i])
            #build embed
            desc = '\n'.join(newlist)
            e = discord.Embed(
                color=await self.bot.get_embed_color(ctx),
                description=f"{desc}",
            )
            e.set_author(name="Paladins stats", icon_url="https://vignette.wikia.nocookie.net/steamtradingcards/images/7/7d/Paladins_Badge_1.png/revision/latest/top-crop/width/300/height/300?cb=20161215201250")
            e.set_footer(text="Data provided by nonsocial.herokuapp.com")
            await ctx.send(embed=e)
            
    @commands.command()
    async def stalk(self, ctx, player, platform="pc"):
        async with self.session.get(f"https://nonsocial.herokuapp.com/api/stalk?player={player}&platform={platform}") as r:
            text = await r.text()
            text = text.replace('-', '|')
            text = re.sub('[()]', '', text)
            text = text.split('| ')
            test = len(text)
            newlist = []
            for i in range(test):
                newlist.append(text[i])
            #build embed
            desc = '\n'.join(newlist)
            e = discord.Embed(
                color=await self.bot.get_embed_color(ctx),
                description=f"{desc}",
            )
            e.set_author(name="Paladins stats", icon_url="https://vignette.wikia.nocookie.net/steamtradingcards/images/7/7d/Paladins_Badge_1.png/revision/latest/top-crop/width/300/height/300?cb=20161215201250")
            e.set_footer(text="Data provided by nonsocial.herokuapp.com")
            await ctx.send(embed=e)
            
            