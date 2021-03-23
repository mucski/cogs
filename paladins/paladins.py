import arez
from PIL import ImageOps, ImageDraw, Image, ImageFont
from redbot.core import commands
import asyncio
import aiohttp
import io
import humanize
from datetime import datetime
import discord
from discord import File


class Paladins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.f = open("/home/ubuntu/key.txt", "r")
        self.auth = self.f.readline()
        self.devid = self.f.readline()
        self.api = arez.PaladinsAPI(dev_id=self.devid.strip(),
                                    auth_key=self.auth.strip())

    def cog_unload(self):
        asyncio.createTask(self.api.close())
        self.f.close()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            exc = error.original
            if isinstance(exc, arez.Unavailable):
                await ctx.send("HiRez API is offline or unavaiable.")
                return
            if isinstance(exc, arez.Private):
                await ctx.send("Requested profile is set to private")
                return
            if isinstance(exc, arez.NotFound):
                await ctx.send("Player was not found")
                return
        await ctx.bot.on_command_error(ctx, error, unhandled_by_cog=True)

    async def get_champ_image(self, champ):
        champ = champ.lower()
        if "bomb" in champ:
            champ = "bomb-king"
        if "sha" in champ:
            champ = "sha-lin"
        if "mal" in champ:
            champ = "maldamba"
        url = "https://web2.hirez.com/paladins/champion-icons/" \
            + str(champ) + ".jpg"
        return url

    async def draw_rectangle(self, img, draw):
        TINT_COLOR = (0, 0, 0)  # Black
        RED_COLOR = (237, 59, 59) # Red
        BLUE_COLOR = (59, 142, 237) # Blu
        TRANSPARENCY = .5  # Degree of transparency, 0-100%
        OPACITY = int(255 * TRANSPARENCY)
        # img = ImageDraw.Draw(img, "RGBA")
        # Determine extent of the largest possible square centered on the image.
        # and the image's shorter dimension.
        if img.size[0] > img.size[1]:
            shorter = img.size[1]
            llx, lly = (img.size[0]-img.size[1]) // 2 , 0
        else:
            shorter = img.size[0]
            llx, lly = 0, (img.size[1]-img.size[0]) // 2

        # Calculate upper point + 1 because second point needs to be just outside the
        # drawn rectangle when drawing rectangles.
        urx, ury = llx+shorter+1, lly+shorter+1
        return draw.rectangle(((llx, lly), (urx, ury)), fill=RED_COLOR+(OPACITY,))
        # out = Image.alpha_composite(out, overlay)

    async def stats_image(self, champ_icon, champ_stats, index, party):
        shrink = 140
        offset = 10
        image_size_y = 512 - shrink * 2
        img_x = 512
        middle = image_size_y/2 - 50
        im_color = (175, 238, 238, 0) if index % 2 == 0 else (196, 242, 242, 0)
        img = Image.new("RGBA", (img_x*9, image_size_y+offset*2), color=(175, 238, 238, 0))
        draw = ImageDraw.Draw(img)
        img.paste(champ_icon, (0, 0, offset, offset))
        fnt80 = ImageFont.truetype("home/ubuntu/arial.ttf", 80)
        fnt100 = ImageFont.truetype("home/ubuntu/arial.ttf", 100)
        fill = (0, 0, 0)
        # Champion name, player name
        draw.text((img_x+20, middle-40), str(champ_stats[0]), font=fnt80, fill=fill)
        draw.text((img_x+20, middle+60), str(champ_stats[1]), font=fnt80, fill=fill)
        # Parties
        draw.text((img_x+750, middle), champ_stats[2], font=fnt100, fill=fill)
        # Credits
        draw.text((img_x+900, middle), champ_stats[3], font=fnt100, fill=fill)
        # KDA
        draw.text((img_x+1300, middle), champ_stats[4], font=fnt100, fill=fill)
        # Damage Done
        draw.text((img_x+1830, middle), champ_stats[5], font=fnt100, fill=fill)
        # Mitigated
        draw.text((img_x+2350, middle), champ_stats[6], font=fnt100, fill=fill)
        # OBJ time
        draw.text((img_x+2850, middle), champ_stats[7], font=fnt100, fill=fill)
        # Shielding
        draw.text((img_x+3150, middle), champ_stats[8], font=fnt100, fill=fill)
        # Healing
        draw.text((img_x+3600, middle), champ_stats[9], font=fnt100, fill=fill)
        return stats_image


    @commands.command()
    async def hitest(self, ctx, map):
        out = Image.open(f"home/ubuntu/icons/maps/{map}.png")
        # overlay = Image.new("RGBA", out.size, TINT_COLOR+(0,))
        draw = ImageDraw.Draw(out, "RGBA")
        await self.draw_rectangle(out, draw)
        champ_icon = await self.get_champ_image("jenos")
        champ_stats = ["Jenos", "Joey", "1", "4000", "24/1/24", "394923", "39394", "222", "0", "0"]
        index = 1
        party = 1
        await self.stats_image(champ_icon, champ_stats, index, party)
        # save it to buffer
        buffer = io.BytesIO()
        # save PNG in buffer
        out.save(buffer, format='PNG')
        # move to beginning of buffer so `send()` it will read from beginning
        buffer.seek(0)
        # send image
        await ctx.send(file=File(buffer, 'yourmom.jpg'))

    @commands.command()
    async def stats(self, ctx, player, platform="PC"):
        platform = arez.Platform(platform)
        if player.isdecimal():
            player = await self.api.get_player(player)
        else:
            player_obj = await self.api.search_players(player, platform)
            player = await player_obj[0]
        desc = (
            "**__Player Stats__**\n"
            f"```Account level: {player.level}\n"
            f"Playtime: {int(player.playtime.total_hours())} hours\n"
            f"Region: {player.region}\n"
            f"Champions Owned: {player.champion_count}\n"
            f"Achievements Unlocked: {player.total_achievements}\n"
            f"Account Created: "
            f"{humanize.naturaltime(datetime.utcnow() - player.created_at)}\n"
            f"Last Login: "
            f"{humanize.naturaltime(datetime.utcnow() - player.last_login)}\n"
            "```\n\n"
            f"**__Casual Stats__**\n"
            f"```Win Rate: "
            f"{player.casual.wins}/{player.casual.losses}"
            f" ({player.casual.winrate_text})\n"
            f"Deserted: {player.casual.leaves}\n```"
            "\n\n"
            f"**__Ranked Stats Season {player.ranked_best.season}__**\n"
            f"```Win Rate: "
            f"{player.ranked_best.wins}/{player.ranked_best.losses}"
            f" ({player.ranked_best.winrate_text})\n"
            f"Deserted: {player.ranked_best.leaves}\n"
            f"Ranked Type: {player.ranked_best.type}\n"
            f"Current Rank: {player.ranked_best.rank}"
            f" ({player.ranked_best.points} TP)\n```"
        )
        e = discord.Embed(color=await self.bot.get_embed_color(ctx),
                          title=f"{player.name}({player.platform})"
                                f"_({player.title})_")
        e.description = desc
        e.set_thumbnail(url=player.avatar_url)
        e.set_footer(text=f"Player ID: {player.id}")
        await ctx.send(embed=e)
