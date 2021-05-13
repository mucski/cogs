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
        W, H = (4880, 232)
        #padding or margin size
        padding = 10
        #middle
        mid = int((H - 80) / 2)
        #image background color odd and even
        img_color = (14, 34, 43) if index % 2 == 0 else (15, 40, 48)
        #text fill size 
        fill = (255, 255, 255)
        #new image object
        img = Image.new("RGBA", (W, H), color = img_color)
        #champion icon
        img.paste(champicon, (padding, padding))
        #rank icon
        img.paste(rankicon, (1526, mid), mask = rankicon)
        #make the image drawable
        draw = ImageDraw.Draw(img)
        #normal font
        fnt = ImageFont.truetype("home/ubuntu/arial.ttf", 80)
        #bold font
        fntbld = ImageFont.truetype("home/ubuntu/arialbd.ttf", 80)
        
        #player name and level
        draw.text((512 + padding * 4, mid - 50), str(stats[0]), font=fntbld, color=fill)
        draw.text((512 + padding * 4, mid + 30), str(stats[1]), font=fnt, color=fill)
    
        
        #credits earned
        draw.text((1736, mid), humanize_number(stats[2]), font=fnt, color=fill)
        #kda
        draw.text((2036, mid), stats[3], font=fnt, color=fill)
        #dmg done
        draw.text((2400, mid), humanize_number(stats[4]), font=fnt, color=fill)
        #dmg taken
        draw.text((2800, mid), humanize_number(stats[5]), font=fnt, color=fill)
        #objective
        draw.text((3200, mid), humanize_number(stats[6]), font=fnt, color=fill)
        #shielding
        draw.text((3436, mid), humanize_number(stats[7]), font=fnt, color=fill)
        #healing
        draw.text((3836, mid), humanize_number(stats[8]), font=fnt, color=fill)
        #self healing
        draw.text((4236, mid), humanize_number(stats[11]), font=fnt, color=fill)
        #kda2
        draw.text((4636, mid), "{:.2f}".format(stats[12]), font=fnt, color=fill)
        return img

    @classmethod
    async def playerkey(cls, x, y):
        #the image object
        key = Image.new("RGB", (x, y - 60), color = (8, 21, 25))
        draw = ImageDraw.Draw(key)
        fill = (255, 255, 255)
        padding = 10
        fntbld = ImageFont.truetype("home/ubuntu/arialbd.ttf", 50)
        
        #champion and player
        draw.text((20, 20), "CHAMPION", font = fntbld, fill = fill)
        draw.text((512 + padding * 4, 20), "PLAYER", font = fntbld, fill = fill)
        
        #rank
        draw.text((1576, 20), "R", font = fntbld, fill = fill)
        #credits
        draw.text((1736, 20), "CREDITS", font = fntbld, fill = fill)
        #kda
        draw.text((2036, 20), "K/D/A", font = fntbld, fill = fill)
        #damage done
        draw.text((2400, 20), "DAMAGE", font = fntbld, fill = fill)
        #damage taken
        draw.text((2800, 20), "MITIGATED", font = fntbld, fill = fill)
        #objective
        draw.text((3200, 20), "OBJ", font = fntbld, fill = fill)
        #shielding
        draw.text((3436, 20), "SHIELDING", font = fntbld, fill = fill)
        #healing
        draw.text((3836, 20), "HEALING", font = fntbld, fill = fill)
        #self healing
        draw.text((4236, 20), "SELF HEAL", font = fntbld, fill = fill)
        #kda2
        draw.text((4636, 20), "KDA", font = fntbld, fill = fill)
        return key

    @classmethod
    async def historyimg(cls, team1, team2, t1_data, t2_data, r1, r2, match_data):
        crop = 140
        W, H = (4880, 2960)
        padding = 10
        img = Image.new("RGB", (W, H))
        
        #headers
        key = await helper2.playerkey(W, H)
        img.paste(key, (0, 0))
        
        #middle panel
        middle = await helper2.middlepanel(match_data)
        img.paste(middle, (0, int(H / 2 - 200)))
        
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
            img.paste(playerpanel, (0, 236 * i + 100))
            
            
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
            img.paste(playerpanel, (0, 236 * i + 1792))
        #done, reisizing for speed
        historyimg = img.resize((int(W / 2), int(H / 2)), Image.ANTIALIAS)
        #create the buffer
        final_buffer = BytesIO()
        #store image in buffer
        historyimg.save(final_buffer, "PNG")
        #seek back to start
        final_buffer.seek(0)
        return final_buffer
        
    @classmethod
    async def middlepanel(cls, match_data):
        W, H = (4880, 512)
        padding = 46
        #(horizontal, vertical)
        img = Image.new("RGB", (W, H))
        
        #add in the map image 
        map_name = match_data[3]
        format_map = map_name.lower().replace(" ", "_").replace("'", "")
        try:
            match_map = Image.open(f"home/ubuntu/icons/maps/{format_map}.png")
        except FileNotFoundError:
            match_map = Image.open("home/ubuntu/icons/maps/test_maps.png")
        #middle image width
        basewidth = 4880
        #dynamic resize
        wpercent = (basewidth / float(match_map.size[0]))
        hsize = int((float(match_map.size[1]) * float(wpercent)))
        match_map = match_map.resize((basewidth, hsize), Image.ANTIALIAS)
        #final product
        img.paste(match_map, (0, 0))
        
        draw = ImageDraw.Draw(img)
        fnt = ImageFont.truetype("home/ubuntu/arial.ttf", 100)
        fill = (255, 255, 255)
        stroke = (8, 21, 25)
        stroke_size = 2
        
        draw.text((padding, padding), f"ID: {match_data[0]}", font = fnt, stroke_width = stroke_size, stroke_fill = stroke, fill = fill)
        draw.text((padding, 100 + padding), f"ID: {match_data[0]}", font = fnt, stroke_width = stroke_size, stroke_fill = stroke, fill = fill)
        draw.text((padding, 200 + padding), f"ID: {match_data[0]}", font = fnt, stroke_width = stroke_size, stroke_fill = stroke, fill = fill)
        draw.text((padding, 300 + padding), f"ID: {match_data[0]}", font = fnt, stroke_width = stroke_size, stroke_fill = stroke, fill = fill)
        
        return img