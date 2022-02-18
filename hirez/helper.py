from __future__ import annotations

from PIL import ImageOps, ImageDraw, Image, ImageFont, ImageEnhance
import aiohttp
from io import BytesIO
from redbot.core.utils.chat_formatting import humanize_number

def champ_into_pic(champ: arez.Champion) -> Image:
    name = champ.name.lower().replace(" ","-").replace("'","")
    try:
        pic = Image.open(f"root/mucski/stuff/icons/avatars/{name}.jpg")
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
    mid = int((H - 120) / 2)
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
    # img.paste(rankicon, (1526, mid), mask=rankicon)
    # make the image drawable
    draw = ImageDraw.Draw(img)
    # normal font
    fnt = ImageFont.truetype("root/mucski/stuff/arial.ttf", 80)
    # bold font
    fntbld = ImageFont.truetype("root/mucski/stuff/arialbd.ttf", 80)
    smallfnt = ImageFont.truetype("root/mucski/stuff/arial.ttf", 60)

    name = mp.player.name

    if name == "":
        name = "?????????"

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
    key = Image.new("RGB", (x, y - 60), color=(8, 21, 25))
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

def historyimg(team1, team2, t1_data, t2_data, r1, r2, match_data):
    crop = 140
    W, H = (4620, 2932)
    # padding=10
    img = Image.new("RGB", (W, H), color=(8, 21, 25))

    # headers
    key = playerkey(W, H)
    img.paste(key, (0, 0))

    # middle panel
    middle = middlepanel(match_data)
    img.paste(middle, (0, int(H / 2 - 200)))
    # player data
    for team_num, team in enumerate((team1, team2), start=1):
        if team_num == 1:
            offset = 100
            rank = r1
            team_data = t1_data
        else:
            offset = 1772
            rank = r2
            team_data = t2_data
        for i, champ in enumerate(team):
            # team 1
            try:
                champimg = champ_into_pic(champ)
            except FileNotFoundError:
                champimg = Image.open("root/mucski/stuff/icons/error.jpg")
            if champimg.size < (512, 512):
                (width, height) = (champimg.width * 2, champimg.height * 2)
                champimg = champimg.resize((width, height))
            # cropping champion image
            border = (0, crop, 0, crop)
            champimgcrop = ImageOps.crop(champimg, border)
            # rank icon
            rankicon = Image.open(f"root/mucski/stuff/icons/ranks/{rank[i]}.png")
            # playerstats
            playerpanel = statsimage(champimgcrop, rankicon, team_data[i], i)
            img.paste(playerpanel, (0, 232 * i + offset))
    # done, reisizing for speed
    historyimg = img.resize((int(W / 2), int(H / 2)), Image.ANTIALIAS)
    # historyimg = img.resize((int(W / 2), int(H / 2)))
    # create the buffer
    final_buffer = BytesIO()
    # store image in buffer
    historyimg.save(final_buffer, "PNG")
    # seek back to start
    final_buffer.seek(0)
    return final_buffer

def middlepanel(mp):
    W, H = (4620, 512)
    padding = 46
    # (horizontal, vertical)
    img = Image.new("RGB", (W, H))

    # add in the map image
    map_name = mp.map_name
    format_map = map_name.lower().replace(" ", "_").replace("'", "")
    try:
        match_map = Image.open(f"root/mucski/stuff/icons/maps/{format_map}.png")
    except FileNotFoundError:
        match_map = Image.open("root/mucski/stuff/icons/maps/test_maps.png")
    # middle image width
    basewidth = 4620
    # dynamic resize
    wpercent = (basewidth / float(match_map.size[0]))
    hsize = int((float(match_map.size[1]) * float(wpercent)))
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

    draw.text((padding, padding), f"ID: {mp.id}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((padding, 100 + padding), f"Duration: {mp.duration} min", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((padding, 200 + padding), f"Region: {mp.region}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)
    draw.text((padding, 300 + padding), f"Map: {mp.map_name}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)

    draw.text((int(W / 2 - 1032), padding), f"Team 1 score: {mp.score[1]}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)

    vs = Image.open("root/mucski/stuff/icons/vs.png")
    w, h = vs.size
    vs = vs.resize((int(w * 2 / 3), int(h * 2 / 3)))
    img.paste(vs, (int((W-w) / 2), int((H-h) / 2 + 48)), mask=vs)

    draw.text((int(W / 2 + 173), 300 + padding), f"Team 2 score: {mp.score[2]}", font=fnt, stroke_width=stroke_size, stroke_fill=stroke, fill=fill)

    # ranked bans go here

    return img
