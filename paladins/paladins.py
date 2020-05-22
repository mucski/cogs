import aiohttp
import discord
import asyncio
import re
from redbot.core import commands, Config
from redbot.core.utils.predicates import MessagePredicate

class Paladins(commands.Cog):
    """ If you have a name with spaces in it please wrap it in double quotes like so .last "my long name"
    Champion names with space can be typed as so instead .kda myname bombking or shalin"""
    def __init__(self, bot):
        self.bot = bot
    #thanks DevilXD
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        asyncio.create_task(self.session.close())
           
    # shit rewrite
    # regex is hard plz help
    @commands.command()
    async def last(self, ctx, player, platform="pc"):
        """Shows last played match by ``player``"""
        async with self.session.get(f"https://nonsocial.herokuapp.com/api/lastmatch?player={player}&platform={platform}") as r:
            text = await r.text()
            #pain im the ass regex, domt touch
            text = re.findall(r"([\w]+)([\w?\s]+).*Id:\s(\d+).*tion:\s(\d+)m.*ion:\s([\w\s🇺🇸]+)\W+([\w?:|\w\s?]+)\W+([\d/]+)\s-\s([\d.]+).*ee:\s(\d+).*ge:\s([\d,]+).*ts:\s([\d,]+).*ore:\s([\d/]+)", text)
            if not text:
                await ctx.send(f':x: Wrong player name or platform. If your name contains spaces please use double quotes like so: ``.last "{player}"``')
                return
            avatar = text[0][5].replace(' ', '')
            region = text[0][4].replace('🇺🇸', 'North America')
            if avatar == "bombking" or avatar == "shalin":
                avatar = avatar.replace("bombking", "bomb-king").replace("shalin", "sha-lin")
            avatarurl = f"https://web2.hirez.com/paladins/champion-icons/{avatar.lower()}.jpg"
            if text[0][0] == "Ranked":
                matchType = "Ranked"
            else:
                matchType = "Casual"
            e = discord.Embed(color=await self.bot.get_embed_color(ctx))
            e.set_thumbnail(url=avatarurl)
            e.add_field(name="Map", value=f"{matchType} - {text[0][1]}")
            e.add_field(name="Match Id:", value=text[0][2])
            e.add_field(name="Duration", value=f"{text[0][3]} minutes")
            e.add_field(name="Region", value=region)
            e.add_field(name="Champion", value=text[0][5])
            e.add_field(name="KDA", value=f"{text[0][6]} ({text[0][7]})")
            e.add_field(name="Kill Spree", value=text[0][8])
            e.add_field(name="Damage", value=text[0][9])
            e.add_field(name="Credits", value=text[0][10])
            e.add_field(name="Score", value=text[0][11])
            e.set_author(name=f"Paladins: showing last match", icon_url="https://vignette.wikia.nocookie.net/steamtradingcards/images/7/7d/Paladins_Badge_1.png/revision/latest/top-crop/width/300/height/300?cb=20161215201250")
            e.set_footer(text="Data provided by nonsocial.herokuapp.com")
            await ctx.send(embed=e)
            