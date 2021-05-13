from PIL import ImageOps, ImageDraw, Image, ImageFont
import aiohttp
from io import BytesIO
from redbot.core.utils.chat_formatting import humanize_number
import math

class helper2:
    
    @classmethod
    async def champimg(cls, name):
        name = name.lower()
        if "bomb" in name:
            name = "bomb-king"
        if "sha" in name:
            name = "sha-lin"
        if "mal" in name:
            name = "maldamba"
        url = f"https://webcdn.hirezstudios.com/paladins/champion-icons/{name}.jpg"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    resp = await resp.read()
        return resp

    @classmethod
    async def testchampimg(cls, name):
        name = name.lower()
        if "bomb" in name:
            name = "bomb-king"
        if "sha" in name:
            name = "sha-lin"
        if "mal" in name:
            name = "maldamba"
        url = f"https://webcdn.hirezstudios.com/paladins/champion-icons/{name}.jpg"
        return url

    @classmethod
    async def statsimage(cls, champicon, rankicon, stats, index):
        #crop size
        shrink = 140
        #vertical
        W, H = (512, 232)
        #padding or margin size
        padding = 10
        #middle
        mid = int((H - 80) / 2)
        #image background color odd and even
        img_color = (14, 34, 43) if index % 2 == 0 else (15, 40, 48)
        #text fill size 
        fill = (255, 255, 255)
        #new image object
        img = Image.new("RGBA", (W * 11, H), color = img_color)
        #champion icon
        img.paste(champicon, (padding, padding))
        #rank icon
        img.paste(rankicon, (W * 3, mid), mask = rankicon)
        #make the image drawable
        draw = ImageDraw.Draw(img)
        #normal font
        fnt = ImageFont.truetype("home/ubuntu/arial.ttf", 80)
        #bold font
        fntbld = ImageFont.truetype("home/ubuntu/arialbd.ttf", 80)
        
        #player name and level
        draw.text((W, mid), str(stats[0]), font=fntbld, color=fill)
        draw.text((W, mid - 80), str(stats[1]), font=fnt, color=fill)
    
        
        #credits earned
        draw.text((W * 3, mid), humanize_number(stats[2]), font=fnt, color=fill)
        #kda
        draw.text((W * 4, mid), stats[3], font=fnt, color=fill)
        #dmg done
        draw.text((W * 5, mid), humanize_number(stats[4]), font=fnt, color=fill)
        #dmg taken
        draw.text((W * 6, mid), humanize_number(stats[5]), font=fnt, color=fill)
        #objective
        draw.text((W * 7, mid), humanize_number(stats[6]), font=fnt, color=fill)
        #shielding
        draw.text((W * 8, mid), humanize_number(stats[7]), font=fnt, color=fill)
        #healing
        draw.text((W * 9, mid), humanize_number(stats[8]), font=fnt, color=fill)
        #self healing
        draw.text((W * 10, mid), humanize_number(stats[11]), font=fnt, color=fill)
        #kda2
        draw.text((W * 11, mid), "{:.2f}".format(stats[12]), font=fnt, color=fill)
        return img

    @classmethod
    async def playerkey(cls, x, y):
        #the image object
        key = Image.new("RGB", (x * 11, y - 100), color = (8, 21, 25))
        draw = ImageDraw.Draw(key)
        fill = (255, 255, 255)
        margin = 56
        offset = 256
        padding = 10
        fntbld = ImageFont.truetype("home/ubuntu/arialbd.ttf", 80)
        
        #champion and player
        draw.text((20, 0), "Champion", font = fntbld, fill = fill)
        draw.text((x + padding, 0), "Player", font = fntbld, fill = fill)
        
        #rank
        draw.text((math.floor(x * 3 - x / 3), 0), "R", font = fntbld, fill = fill)
        #credits
        draw.text((x * 3 + margin, 0), "Credits", font = fntbld, fill = fill)
        #kda
        draw.text((x * 4 + margin - offset / 2, 0), "K/D/A", font = fntbld, fill = fill)
        #damage done
        draw.text((x * 5 + margin - offset + offset / 3, 0), "Damage", font = fntbld, fill = fill)
        #damage taken
        draw.text((x * 6 + margin - offset + offset / 3, 0), "Mitigated", font = fntbld, fill = fill)
        #objective
        draw.text((x * 7 + margin - offset + offset / 3, 0), "Obj", font = fntbld, fill = fill)
        #shielding
        draw.text((x * 8 + margin - offset - offset / 4, 0), "Shielding", font = fntbld, fill = fill)
        #healing
        draw.text((x * 9 + margin - offset - offset / 4, 0), "Healing", font = fntbld, fill = fill)
        #self healing
        draw.text((x * 10 + margin - offset - offset / 4, 0), "Self Heal", font = fntbld, fill = fill)
        #kda2
        draw.text((x * 11 + margin - offset - offset / 4, 0), "KDA", font = fntbld, fill = fill)
        return key

    @classmethod
    async def historyimg(cls, team1, team2, t1_data, t2_data, r1, r2, match_data):
        crop = 140
        img_x = 512
        img_y = 512 - crop * 2
        padding = 10
        img = Image.new("RGB", (img_x * 11, img_y * 13))
        
        #headers
        key = await helper2.playerkey(img_x, img_y)
        img.paste(key, (0, 0))
        
        #middle panel
        middle = await helper2.middlepanel(match_data)
        img.paste(middle, (0, int(img_y * 12 / 2)))
        
        #player data
        for i, (champ, champ2) in enumerate(zip(team1, team2)):
            #team 1
            resp = await helper2.champimg(champ)
            champimg = Image.open(BytesIO(resp))
                
            #cropping champion image
            border = (0, crop, 0, crop)
            champimgcrop = ImageOps.crop(champimg, border)
            #rank icon
            rankicon = Image.open(f"home/ubuntu/icons/ranks/{r1[i]}.png")
            #playerstats
            playerpanel = await helper2.statsimage(champimgcrop, rankicon, t1_data[i], i)
            img.paste(playerpanel, (0, img_y * i + 100))
            
            
            #team 2
            resp = await helper2.champimg(champ2)
            champimg = Image.open(BytesIO(resp))
                
            #cropping champion image
            border = (0, crop, 0, crop)
            champimgcrop = ImageOps.crop(champimg, border)
            #rank icon
            rankicon = Image.open(f"home/ubuntu/icons/ranks/{r1[i]}.png")
            #playerstats
            playerpanel = await helper2.statsimage(champimgcrop, rankicon, t1_data[i], i)
            img.paste(playerpanel, (0, int(img_y * i + img_x * 3 + img_x / 2 + img_x / 8)))
        #done, reisizing for speed
        historyimg = img.resize((1920, 1080), Image.ANTIALIAS)
        #create the buffer
        final_buffer = BytesIO()
        #store image in buffer
        historyimg.save(final_buffer, "PNG")
        #seek back to start
        final_buffer.seek(0)
        return final_buffer
        
    @classmethod
    async def middlepanel(cls, match_data):
        crop = 140
        img_x = 512
        img_y = 512
        #(horizontal, vertical)
        img = Image.new("RGB", (img_x * 11, img_y))
        
        #add in the map image 
        map_name = match_data[3]
        format_map = map_name.lower().replace(" ", "_").replace("'", "")
        try:
            match_map = Image.open(f"home/ubuntu/icons/maps/{format_map}.png")
        except FileNotFoundError:
            match_map = Image.open("home/ubuntu/icons/maps/test_maps.png")
        #middle image width
        basewidth = img_x * 11
        #dynamic resize
        wpercent = (basewidth / float(match_map.size[0]))
        hsize = int((float(match_map.size[1]) * float(wpercent)))
        match_map = match_map.resize((basewidth, hsize), Image.ANTIALIAS)
        #final product
        img.paste(match_map, (0, 0))
        
        draw = ImageDraw.Draw(img)
        fnt = ImageFont.truetype("home/ubuntu/arial.ttf", 80)
        fill = (255, 255, 255)
        stroke = (8, 21, 25)
        stroke_size = 2
        
        draw.text((0, img_y), f"ID: {match_data[0]}", font = fnt, stroke_width = stroke_size, stroke_fill = stroke, fill = fill)
        
        return img