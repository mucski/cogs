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

    @commands.command()
    async def hitest(self, ctx, map):
        TINT_COLOR = (0, 0, 0)  # Black
        TRANSPARENCY = .25  # Degree of transparency, 0-100%
        OPACITY = int(255 * TRANSPARENCY)
        # shrink = 140
        # offset = 10
        # image_size_y = 512 - shrink * 2
        # img_x = 512
        # middle = image_size_y/2 - 50
        # Sum test
        # create an image
        # out = Image.new("RGBA", (img_x*4, image_size_y+offset*2), (3, 177, 252))
        out = Image.open(f"home/ubuntu/icons/maps/{map}.png")
        out.convert("RGBA")
        # (width, height) = (img_x * 4, image_size_y+offset * 2)
        # resize_bg = background.resize((width, height))
        # out.paste(resize_bg, (0, 0), resize_bg)

        # get a font
        fnt = ImageFont.truetype("home/ubuntu/arial.ttf", 40)
        # get a drawing context
        image = ImageDraw.Draw(out)

        versus = Image.open("home/ubuntu/icons/vs.png")
        (width, height) = (versus.width // 5, versus.height // 5)
        resized_versus = versus.resize((width, height))
        out.paste(resized_versus, (10, 10), resized_versus)
        if out.size[0] > out.size[1]:
            shorter = out.size[1]
            llx, lly = (out.size[0]-out.size[1]) // 2 , 0
        else:
            shorter = out.size[0]
            llx, lly = 0, (out.size[1]-out.size[0]) // 2

        urx, ury = llx+shorter+1, lly+shorter+1

        overlay = Image.new("RGBA", out.size, TINT_COLOR+(0,))
        draw = Image.draw(overlay)
        draw.rectangle(((llx, lly), (urx, ury)), fill=TINT_COLOR+(OPACITY,))
        Image.alpha_composite(out, overlay)

        # draw multiline text
        image.multiline_text((10, 10), f"Hello\nWorld", font=fnt, fill=(0, 0, 0))

        # save it to buffer
        buffer = io.BytesIO()
        # save PNG in buffer
        image.save(buffer, format='PNG')
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
