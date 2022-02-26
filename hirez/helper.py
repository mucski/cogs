from __future__ import annotations

from PIL import ImageOps, ImageDraw, Image, ImageFont, ImageEnhance
import aiohttp
from io import BytesIO
from redbot.core.utils.chat_formatting import humanize_number
import imageio as iio

def champ_into_pic(champ: arez.Champion) -> Image:
    name = champ.name.lower().replace(" ","-").replace("'","")
    try:
        pic = Image.open(f"root/mucski/stuff/icons/avatars/{name}.jpg")
        if pic.size < (512, 512):
            (width, height) = (pic.width * 2, pic.height * 2)
            pic = pic.resize((width, height))
    except FileNotFoundError:
        pic = Image.open("root/mucski/stuff/icons/error.jpg")
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
        rankicon = Image.open(f"root/mucski/stuff/icons/ranks/99.png")
    else:
        rankicon = Image.open(f"root/mucski/stuff/icons/ranks/{mp.player.ranked_best.rank.value}.png")
    img.paste(rankicon, (1526, mid), mask=rankicon)
    # make the image drawable
    draw = ImageDraw.Draw(img)
    # normal font
    fnt = ImageFont.truetype("root/mucski/stuff/arial.ttf", 80)
    # bold font
    fntbld = ImageFont.truetype("root/mucski/stuff/arialbd.ttf", 80)
    smallfnt = ImageFont.truetype("root/mucski/stuff/arial.ttf", 60)

    name = mp.player.name

    if name == "":
        name = "???"

    # player name and level
    draw.text((512 + padding * 4, mid - 30), name, font=fntbld, fill=color)
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
    draw.text((4256, mid), humanize_number(mp.healing_self), font=fnt, fill=fill)
    # kda2
    # draw.text((4636, mid), "{:.2f}".format(stats[12]), font=fnt, fill=fill)
    return img

def playerkey(x, y):
    # the image object
    key = Image.new("RGB", (x, y), color=(8, 21, 25))
    draw = ImageDraw.Draw(key)
    fill = (255, 255, 255)
    padding = 10
    fntbld = ImageFont.truetype("root/mucski/stuff/arialbd.ttf", 50)

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
    historyimg = img.resize((2310, 1471), Image.ANTIALIAS)
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
        match_map = Image.open(f"root/mucski/stuff/icons/maps/{format_map}.png")
    except FileNotFoundError:
        match_map = Image.open("root/mucski/stuff/icons/maps/test_maps.png")
    # middle image width
    basewidth = 4620
    # dynamic resize
    wpercent = (basewidth / float(match_map.size[0]))
    hsize = round((float(match_map.size[1]) * float(wpercent)))
    match_map = match_map.resize((basewidth, hsize), Image.ANTIALIAS)

    enhancer = ImageEnhance.Brightness(match_map)
    match_map = enhancer.enhance(0.5)
    # final product
    img.paste(match_map, (0, -512))

    draw = ImageDraw.Draw(img)
    fnt = ImageFont.truetype("root/mucski/stuff/arial.ttf", 100)
    #fill = (15, 40, 48) dark
    fill = (255, 255, 255)
    stroke = (255, 255, 255)
    stroke_size = 0

    draw.text((padding, padding), f"ID: {match.id}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((padding, 100 + padding), f"Duration: {match.duration}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((padding, 200 + padding), f"Region: {match.region}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((padding, 300 + padding), f"Map: {match.map_name}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)

    draw.text((round(W / 2 - 1032), padding), f"Team 1 score: {match.score[0]}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)

    vs = Image.open("root/mucski/stuff/icons/vs.png")
    w, h = vs.size
    vs = vs.resize((round(w * 2 / 3), round(h * 2 / 3)))
    img.paste(vs, (round((W-w) / 2), round((H-h) / 2 + 48)), mask=vs)

    draw.text((round(W / 2 + 173), 300 + padding), f"Team 2 score: {match.score[1]}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)

    if match.bans:
        draw.text((round((W-w) / 2) + 1520, round((H-h) / 2) + 80), "Bans", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)

        for i, ban in enumerate(match.bans):
            if i == 0:
                #### Champion 1 ####
                champicon = champ_into_pic(ban)
                champicon = champicon.resize((200, 200))
                img.paste(champicon, (round((W-w) / 2) + 1800, round((H-h) / 2) - 70))
            elif i == 1:
                #### Champion 2 ####
                champicon2 = champ_into_pic(ban)
                champicon2 = champicon2.resize((200, 200))
                img.paste(champicon2, (int((W-w) / 2) + 2020, int((H-h) / 2) - 70))
            elif i == 2:
                #### Champion 3 ####
                champicon3 = champ_into_pic(ban)
                champicon3 = champicon3.resize((200, 200))
                img.paste(champicon3, (int((W-w) / 2) + 2240, int((H-h) / 2) - 70))
            elif i == 3:
                #### CHAMPION 4 ####
                champicon4 = champ_into_pic(ban)
                champicon4 = champicon4.resize((200, 200))
                img.paste(champicon4, (int((W-w) / 2) + 1800, int((H-h) / 2) + 150))
            elif i == 4:
                #### Champion 5 ####
                champicon5 = champ_into_pic(ban)
                champicon5 = champicon5.resize((200, 200))
                img.paste(champicon5, (int((W-w) / 2) + 2020, int((H-h) / 2) + 150))
            elif i == 5:
                #### Champion 6 ####
                champicon6 = champ_into_pic(ban)
                champicon6 = champicon6.resize((200, 200))
                img.paste(champicon6, (int((W-w) / 2) + 2240, int((H-h) / 2) + 150))
    return img

def getavatar(player):
    avatar = imread(player.avatar_url)
    
def generatecard(player):
    W, H = 1080, 1920
    img = Image.new("RGB", (W, H))
    padding = 40
    avatar_img = iio.imread(iio.core.urlopen(player.avatar_url).read(), ".png")
    avatar = Image.open(avatar_img)
    img.paste(avatar, (0, 512))
    draw = ImageDraw.Draw(img)
    fnt = ImageFont.truetype("root/mucski/stuff/arial.ttf", 60)
    #fill = (15, 40, 48) dark
    fill = (255, 255, 255)
    stroke = (255, 255, 255)
    stroke_size = 0
    # name
    draw.text((padding, padding), f"{player.name}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((padding, padding + 120), f"Region: {player.region}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((padding, padding + 240), f"Level: {player.calculated_level}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((padding, padding + 360), "Casual", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((padding, padding + 480), f"WR: {player.casual.winrate_text}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((padding, padding + 600), f"Ranked Season {player.ranked_best.season}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((padding, padding + 720), f"Rank: {player.ranked_best.rank}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    final_buffer = BytesIO()
    img.save(final_buffer, "PNG")
    final_buffer.seek(0)
    return final_buffer