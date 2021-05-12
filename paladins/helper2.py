from PIL import ImageOps, ImageDraw, Image, ImageFont
import aiohttp
from io import BytesIO
from redbot.core.utils.chat_formatting import humanize_number

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
        img_y = 512 - shrink * 2
        #horizontal
        img_x = 512
        #padding or margin size
        padding = 10
        #vertical middle
        middle = img_y / 2
        #image background color odd and even
        img_color = (14, 34, 43) if index % 2 == 0 else (15, 40, 48)
        #text fill size 
        fill = (255, 255, 255)
        #new image object
        img = Image.new("RGBA", (img_x * 11, img_y), color = img_color)
        #champion icon
        img.paste(champicon, (padding, padding))
        #rank icon
        img.paste(rankicon, (1300, middle), mask = rankicon)
        #make the image drawable
        draw = ImageDraw.Draw(img)
        #normal font
        fnt = ImageFont.truetype("home/ubuntu/arial.ttf", 80)
        #bold font
        fntbld = ImageFont.truetype("home/ubuntu/arialbd.ttf", 80)
        
        #player name and level
        draw.text((img_x, middle - 40), str(stats[0]), font=fntbld, color=fill)
        draw.text((img_x, middle + 60), str(stats[1]), font=fnt, color=fill)
        
        #credits earned
        draw.text((img_x * 2, middle), str(stats[2]), font=fnt, color=fill)
        #kda
        draw.text((img_x * 3, middle), str(stats[3]), font=fnt, color=fill)
        #dmg done
        draw.text((img_x * 4, middle), str(stats[4]), font=fnt, color=fill)
        #dmg taken
        draw.text((img_x * 5, middle), str(stats[5]), font=fnt, color=fill)
        #objective
        draw.text((img_x * 6, middle), str(stats[6]), font=fnt, color=fill)
        #shielding
        draw.text((img_x * 7, middle), str(stats[7]), font=fnt, color=fill)
        #healing
        draw.text((img_x * 8, middle), str(stats[8]), font=fnt, color=fill)
        #self healing
        draw.text((img_x * 9, middle), str(stats[9]), font=fnt, color=fill)
        #kda2
        draw.text((img_x * 10, middle), str(stats[10]), font=fnt, color=fill)
        return img

    @classmethod
    async def playerkey(cls, x, y):
        #the image object
        key = Image.new("RGB", (x * 10, y), color = (8, 21, 25))
        draw = ImageDraw.Draw(key)
        fill = (255, 255, 255)
        fntbld = ImageFont.truetype("home/ubuntu/arialbd.ttf", 80)
        
        #champion and player
        draw.text((20, 0), "Champion", font = fntbld, fill = fill)
        draw.text((x, 0), "Player", font = fntbld, fill = fill)
        
        #rank
        draw.text((x * 2, 0), "R", font = fntbld, fill = fill)
        #credits
        draw.text((x * 3, 0), "Credits", font = fntbld, fill = fill)
        #kda
        draw.text((x * 4, 0), "K/D/A", font = fntbld, fill = fill)
        #damage done
        draw.text((x * 5, 0), "Damage", font = fntbld, fill = fill)
        #damage taken
        draw.text((x * 6, 0), "Mitigated", font = fntbld, fill = fill)
        #objective
        draw.text((x * 7, 0), "Objective", font = fntbld, fill = fill)
        #shielding
        draw.text((x * 8, 0), "Shielding", font = fntbld, fill = fill)
        #healing
        draw.text((x * 9, 0), "Healing", font = fntbld, fill = fill)
        #self healing
        draw.text((x * 10, 0), "Self Heal", font = fntbld, fill = fill)
        #kda2
        draw.text((x * 11, 0), "K/D/A2", font = fntbld, fill = fill)
        return key

    @classmethod
    async def historyimg(cls, team1, team2, t1_data, t2_data, r1, r2, match_data):
        crop = 140
        img_x = 512
        img_y = 512 - crop * 2
        padding = 10
        img = Image.new("RGB", (img_x * 10, img_y * 11))
        
        #headers
        key = await helper2.playerkey(img_x, img_y)
        img.paste(key, (0, 0))
        
        #middle panel
        middle = await helper2.middlepanel(match_data)
        img.paste(middle, (0, img_y * 3))
        
        #player data
        for i, (champ, champ2) in enumerate(zip(team1, team2)):
            #team 1
            try:
                resp = await helper2.champimg(champ)
                champimg = Image.open(BytesIO(resp))
                
                #cropping champion image
                border = (0, crop, 0, crop)
                champimgcrop = ImageOps.crop(champimg, border)
                #rank icon
                rankicon = Image.open(f"home/ubuntu/icons/ranks/{r1[i]}.png")
                #playerstats
                playerpanel = await helper2.statsimage(champimgcrop, rankicon, t1_data[i], i)
                img.paste(playerpanel, (0, img_y * i))
            #team 2
            try:
                resp = await helper2.champimg(champ2)
                champimg = Image.open(BytesIO(resp))
                
                #cropping champion image
                border = (0, crop, 0, crop)
                champimgcrop = ImageOps.crop(champimg, border)
                #rank icon
                rankicon = Image.open(f"home/ubuntu/icons/ranks/{r1[i]}.png")
                #playerstats
                playerpanel = await helper2.statsimage(champimgcrop, rankicon, t1_data[i], i)
                img.paste(playerpanel, (0, img_y * i + img_x))
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
        img_y = 512 - crop * 2
        #(horizontal, vertical)
        img = Image.new("RGB", (img_x * 10, img_x))
        return img