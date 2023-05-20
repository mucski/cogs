from __future__ import annotations

from PIL import ImageOps, ImageDraw, Image, ImageFont, ImageEnhance
import aiohttp
import asyncio
from io import BytesIO
from redbot.core.utils.chat_formatting import humanize_number
import humanize
from datetime import datetime
from bs4 import BeautifulSoup


def champ_into_pic(champ: arez.Champion) -> Image:
    name = champ.name.lower().replace(" ","-").replace("'","")
    try:
        pic = Image.open(f"/home/poopski/mucski/stuff/icons/avatars/{name}.jpg")
        if pic.size < (512, 512):
            (width, height) = (pic.width * 2, pic.height * 2)
            pic = pic.resize((width, height))
    except FileNotFoundError:
        pic = Image.open("/home/poopski/mucski/stuff/icons/error.jpg")
    return pic

def statsimage(mp, index):
    crop = 140
    # vertical
    W, H = (4620, 232)
    # padding or margin size
    padding = 10
    # middle
    mid = 61
    # image background color odd and even
    img_color = (14, 34, 43) if index % 2 == 0 else (15, 40, 48)
    # text fill size )
    fill = (255, 255, 255)

    orange = (252, 186, 3)
    green = (7, 252, 3)
    red = (252, 102, 3)
    purple = (240, 3, 252)
    fill = (255, 255, 255)

    if mp.party_number == 1:
        color = green
    elif mp.party_number == 2:
        color = orange
    elif mp.party_number == 3:
        color = purple
    elif mp.party_number == 4:
        color = red
    else:
        color = fill

    # new image object
    img = Image.new("RGBA", (W, H), color=img_color)
    # champion icon
    champicon = champ_into_pic(mp.champion)
    border = (0, crop, 0, crop)
    champimgcrop = ImageOps.crop(champicon, border)
    img.paste(champimgcrop, (padding, padding))
    # rank icon
    if mp.player.private:
        rankicon = Image.open(f"/home/poopski/mucski/stuff/icons/ranks/99.png")
    else:
        rankicon = Image.open(f"/home/poopski/mucski/stuff/icons/ranks/{mp.player.ranked_best.rank.value}.png")
    img.paste(rankicon, (1526, mid), mask=rankicon)
    # make the image drawable
    draw = ImageDraw.Draw(img)
    # normal font
    fnt = ImageFont.truetype("/home/poopski/mucski/stuff/arial.ttf", 80)
    # bold font
    fntbld = ImageFont.truetype("/home/poopski/mucski/stuff/arialbd.ttf", 80)
    smallfnt = ImageFont.truetype("/home/poopski/mucski/stuff/arial.ttf", 60)

    name = mp.player.name

    if name == "":
        name = "???"
    # player name and level
    draw.text((512 + padding * 4, mid - 30), name, font=fntbld, fill=color)
    try:
        draw.text((512 + padding * 4, mid + 60), humanize_number(mp.player.calculated_level), font=smallfnt, fill=fill)
    except AttributeError:
        draw.text((512 + padding * 4, mid + 60), humanize_number(mp.account_level), font=smallfnt, fill=fill)
    # credits earned
    draw.text((1736, mid), humanize_number(mp.credits), font=fnt, fill=fill)
    # kda
    draw.text((2036, mid), mp.kda_text, font=fnt, fill=(224, 197, 135))
    # dmg done
    draw.text((2436, mid), humanize_number(mp.damage_done), font=fnt, fill=fill)
    # dmg taken
    draw.text((2826, mid), humanize_number(mp.damage_taken), font=fnt, fill=fill)
    # objective
    draw.text((3226, mid), humanize_number(mp.objective_time), font=fnt, fill=fill)
    # shielding
    draw.text((3456, mid), humanize_number(mp.shielding), font=fnt, fill=fill)
    # healing
    draw.text((3856, mid), humanize_number(mp.healing_done), font=fnt, fill=fill)
    # self healing
    draw.text((4256, mid), humanize_number(mp.player.ranked_best.type), font=fnt, fill=fill)
    # kda2
    # draw.text((4636, mid), "{:.2f}".format(stats[12]), font=fnt, fill=fill)
    return img

def playerkey(x, y):
    # the image object
    key = Image.new("RGB", (x, y), color=(8, 21, 25))
    draw = ImageDraw.Draw(key)
    fill = (255, 255, 255)
    padding = 10
    fntbld = ImageFont.truetype("/home/poopski/mucski/stuff/arialbd.ttf", 50)

    # champion and player
    draw.text((20, 20), "CHAMPION", font=fntbld, fill=fill)
    draw.text((512 + padding * 4, 20), "PLAYER", font=fntbld, fill=fill)

    # rank
    draw.text((1576, 20), "R", font=fntbld, fill=fill)
    # credits
    draw.text((1736, 20), "CREDITS", font=fntbld, fill=fill)
    # kda
    draw.text((2036, 20), "K/D/A", font=fntbld, fill=fill)
    # damage done
    draw.text((2436, 20), "DAMAGE", font=fntbld, fill=fill)
    # damage taken
    draw.text((2826, 20), "TAKEN", font=fntbld, fill=fill)
    # objective
    draw.text((3226, 20), "OBJ", font=fntbld, fill=fill)
    # shielding
    draw.text((3456, 20), "SHIELDING", font=fntbld, fill=fill)
    # healing
    draw.text((3856, 20), "HEALING", font=fntbld, fill=fill)
    # self healing
    draw.text((4256, 20), "SELF HEAL", font=fntbld, fill=fill)
    # kda2
    # draw.text((4636, 20), "KDA", font=fntbld, fill=fill)
    return key

def format_match(match: arez.Match) -> Image:
    W, H = (4620, 2942)
    # padding=10
    img = Image.new("RGB", (W, H), color=(8, 21, 25))
    # headers
    key = playerkey(4620, 98)
    img.paste(key, (0, 0))
    # format in the players
    for team_num in range(1, 3):  # 1 then 2
        yoffset = (team_num - 1) * 1684 + 98 # replace 1000 with whatever offset you'll need
        team = getattr(match, f"team{team_num}")
        for i, mp in enumerate(team):
            y = i * 232 + yoffset  # replace 50 with whatever row height you use
            row = statsimage(mp, i)  # your current playerkey
            img.paste(row, (0, y))
            # base.paste(row, 0, y)
    # add middlebar
    middle = middlepanel(match)
    img.paste(middle, (0, 1262))
    #base.paste(middlebar(match))
    historyimg = img.resize((2310, 1471), Image.Resampling.LANCZOS)
    final_buffer = BytesIO()
    historyimg.save(final_buffer, "PNG")
    final_buffer.seek(0)
    return final_buffer

def middlepanel(match):
    W, H = (4620, 512)
    padding = 46
    # (horizontal, vertical)
    img = Image.new("RGB", (W, H))

    # add in the map image
    map_name = match.map_name
    format_map = map_name.lower().replace(" ", "_").replace("'", "")
    try:
        match_map = Image.open(f"/home/poopski/mucski/stuff/icons/maps/{format_map}.png")
    except FileNotFoundError:
        match_map = Image.open("/home/poopski/mucski/stuff/icons/maps/test_maps.png")
    # middle image width
    basewidth = 4620
    # dynamic resize
    wpercent = (basewidth / float(match_map.size[0]))
    hsize = round((float(match_map.size[1]) * float(wpercent)))
    match_map = match_map.resize((basewidth, hsize), Image.Resampling.LANCZOS)

    enhancer = ImageEnhance.Brightness(match_map)
    match_map = enhancer.enhance(0.5)
    # final product
    img.paste(match_map, (0, -512))

    draw = ImageDraw.Draw(img)
    fnt = ImageFont.truetype("/home/poopski/mucski/stuff/arial.ttf", 100)
    #fill = (15, 40, 48) dark
    fill = (255, 255, 255)
    stroke = (255, 255, 255)
    stroke_size = 0

    draw.text((padding, padding), f"ID: {match.id}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((padding, 100 + padding), f"Duration: {match.duration}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((padding, 200 + padding), f"Region: {match.region}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((padding, 300 + padding), f"Map: {match.map_name}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)

    draw.text((round(W / 2 - 1032), padding), f"Team 1 score: {match.score[0]}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)

    vs = Image.open("/home/poopski/mucski/stuff/icons/vs.png")
    w, h = vs.size
    vs = vs.resize((round(w * 2 / 3), round(h * 2 / 3)))
    img.paste(vs, (round((W-w) / 2), round((H-h) / 2 + 48)), mask=vs)

    draw.text((round(W / 2 + 173), 300 + padding), f"Team 2 score: {match.score[1]}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)

    if match.bans:
        draw.text((round((W-w) / 2) + 1520, round((H-h) / 2) + 80), "Bans", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)

        for i, ban in enumerate(match.bans):
            if i == 0 and ban != None:
                #### Champion 1 ####
                champicon = champ_into_pic(ban)
                champicon = champicon.resize((200, 200))
                img.paste(champicon, (round((W-w) / 2) + 1800, round((H-h) / 2) - 70))
            elif i == 1 and ban != None:
                #### Champion 2 ####
                champicon2 = champ_into_pic(ban)
                champicon2 = champicon2.resize((200, 200))
                img.paste(champicon2, (int((W-w) / 2) + 2020, int((H-h) / 2) - 70))
            elif i == 2 and not None:
                #### Champion 3 ####
                champicon3 = champ_into_pic(ban)
                champicon3 = champicon3.resize((200, 200))
                img.paste(champicon3, (int((W-w) / 2) + 2240, int((H-h) / 2) - 70))
            elif i == 3 and ban != None:
                #### CHAMPION 4 ####
                champicon4 = champ_into_pic(ban)
                champicon4 = champicon4.resize((200, 200))
                img.paste(champicon4, (int((W-w) / 2) + 1800, int((H-h) / 2) + 150))
            elif i == 4 and ban != None:
                #### Champion 5 ####
                champicon5 = champ_into_pic(ban)
                champicon5 = champicon5.resize((200, 200))
                img.paste(champicon5, (int((W-w) / 2) + 2020, int((H-h) / 2) + 150))
            elif i == 5 and ban != None:
                #### Champion 6 ####
                champicon6 = champ_into_pic(ban)
                champicon6 = champicon6.resize((200, 200))
                img.paste(champicon6, (int((W-w) / 2) + 2240, int((H-h) / 2) + 150))
            else: 
                pass
    return img

async def getavatar(player):
    size = (150, 150)
    async with aiohttp.ClientSession() as session:
        async with session.get(player.avatar_url) as resp:
            if resp.status == 200:
                resp = await resp.read()
    try: # in case heroku goes to shit like always
        avatar = Image.open(BytesIO(resp)).convert("RGBA")
    except TypeError:
        avatar = Image.open("/home/poopski/mucski/stuff/icons/0.png")
    avatar = avatar.resize((150, 150))
    mask = Image.new('L', size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0) + size, fill=255)
    output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output

async def generatecard(player):
    W, H = 860, 1349
    img = Image.open("/home/poopski/mucski/stuff/card_bg.png").convert("RGBA")
    # img = Image.new("RGBA", (W, H))
    avatar = await getavatar(player)
    rank = Image.open(f"/home/poopski/mucski/stuff/icons/ranks2/{player.ranked_best.rank.value}.png")
    img.paste(avatar, (355, 18), mask=avatar)
    img.paste(rank, (350, 1141), mask=rank)
    draw = ImageDraw.Draw(img)
    fnt = ImageFont.truetype("/home/poopski/mucski/stuff/arial.ttf", 37)
    fnt_big = ImageFont.truetype("/home/poopski/mucski/stuff/arial.ttf", 64)
    fnt_small = ImageFont.truetype("/home/poopski/mucski/stuff/arial.ttf", 34)
    #fill = (15, 40, 48) dark
    fill = (126, 163, 215)
    stroke = (23, 34, 50)
    stroke_size = 1
    # name
    kda = await get_kda_guru(player.id)
    if kda:
        kda = kda[3]
    else:
        kda = "?"
    draw.text((33, 211), f"{player.name}", font=fnt_big, stroke_width=stroke_size, stroke_fill=stroke, fill=(180, 160, 138))
    draw.text((33, 277), f"{player.title}  - (Global KDA: {kda})", font=fnt_small, stroke_width=stroke_size, stroke_fill=stroke, fill=(223, 142, 53))
    draw.text((33, 360), f"Level: {player.calculated_level}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((33, 417), f"Region: {player.region}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((33, 474), f"Champions Owned: {player.champion_count}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((33, 531), f"Account Created: {humanize.naturaltime(datetime.utcnow() - player.created_at)}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((33, 588), f"Last Login: {humanize.naturaltime(datetime.utcnow() - player.last_login)}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    # divider = Image.open("root/mucski/stuff/icons/divider.png").convert("RGBA")
    # img.paste(divider, (180, 665), mask=divider)
    # text divider
    draw.text((33, 645), "------------------------------------------------------------------", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((33, 705), f"Casual Winrate: {player.casual.wins}/{player.casual.losses} ({player.casual.winrate_text})", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((33, 762), f"Casual Deserted: {player.casual.leaves}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((33, 819), "------------------------------------------------------------------", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((33, 879), f"Ranked Winrate: {player.ranked_best.wins}/{player.ranked_best.losses} ({player.ranked_best.winrate_text})", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((33, 936), f"Ranked Deserted: {player.ranked_best.leaves}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((33, 993), f"Current Rank: {player.ranked_best.rank} ({player.ranked_best.points} TP)", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=(149, 229, 242))
    draw.text((33, 1050), f"Ranked Type: {player.ranked_best.type}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    final_buffer = BytesIO()
    img.save(final_buffer, "PNG")
    final_buffer.seek(0)
    return final_buffer

async def get_kda_guru(player): # this input must be the player ID
    url = 'https://paladins.guru/profile/{}'.format(player)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                raw = await resp.text()
                soup = BeautifulSoup(raw, 'html.parser')
                stats = []
                for stat in soup.find_all("div", {"class":"tsw__grid__stat"}):
                    stats.append(stat.text)
                return stats
