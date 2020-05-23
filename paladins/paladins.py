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
            match = re.match(r"(\w+) ([\w? ]+) \([\w ]+: (\d+) \| \w+: (\d+)m \| \w+: ([\w 🇺🇸]+)\): ([\w ]+) \(([\d/]+) - ([\d.]+) KDA\) [\w ]+: (\d+) \| \w+: ([\d,]+) \| \w+: ([\d,]+) - \w+ \(\w+: ([\d/]+)\)", text)
            if not match:
                await ctx.send(f':x: Wrong player name or platform. If your name contains spaces please use double quotes like so: ``.last "{player}"``')
                return
            region = match[5].replace('🇺🇸', 'North America')
            avatar = match[6].replace(' ', '-').lower()
            avatarurl = f"https://web2.hirez.com/paladins/champion-icons/{avatar}.jpg"
            if match[1] == "Ranked":
                matchType = "Ranked"
            else:
                matchType = "Casual"
            e = discord.Embed(color=await self.bot.get_embed_color(ctx))
            e.set_thumbnail(url=avatarurl)
            e.add_field(name="Map", value=f"{matchType} - {match[2]}")
            e.add_field(name="Match Id:", value=match[3])
            e.add_field(name="Duration", value=f"{match[4]} minutes")
            e.add_field(name="Region", value=region)
            e.add_field(name="Champion", value=match[6])
            e.add_field(name="KDA", value=f"{match[7]} ({match[8]})")
            e.add_field(name="Kill Spree", value=match[9])
            e.add_field(name="Damage", value=match[10])
            e.add_field(name="Credits", value=match[11])
            e.add_field(name="Score", value=match[12])
            e.set_author(name=f"Paladins: showing last match", icon_url="https://vignette.wikia.nocookie.net/steamtradingcards/images/7/7d/Paladins_Badge_1.png/revision/latest/top-crop/width/300/height/300?cb=20161215201250")
            e.set_footer(text="Data provided by nonsocial.herokuapp.com")
            await ctx.send(embed=e)