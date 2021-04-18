from PIL import ImageOps, ImageDraw, Image, ImageFont
import aiohttp
from io import BytesIO
import requests
from redbot.core.utils.chat_formatting import humanize_number

class helper2:
    
    @classmethod
    async def testing(cls):
        return "Hello World"
        
    @classmethod
    async def get_champ_icon(cls, champ):
        champ = champ.lower()
        if "bomb" in champ:
            champ = "bomb-king"
        if "sha" in champ:
            champ = "sha-lin"
        if "mal" in champ:
            champ = "maldamba"
        url = f"https://webcdn.hirezstudios.com/paladins/champion-icons/{champ}.jpg"
        response = requests.get(url)
        champ_image = Image.open(BytesIO(response.content))
        return champ_image

    @classmethod
    async def player_key(cls, items):
        width, height = 300, 400
        middle = width / 2
        color = (8, 21, 25)
        img = Image.new("RGBA", (width, height), color=color)
        draw = ImageDraw.Draw(img)
        fnt = ImageFont.truetype("home/ubuntu/arialbd.ttf", 30)
        for line in items:
            w, h = draw.textsize(line, font=fnt)
            draw.text(((width - w) / 2, 0), line, font=fnt, fill=(255, 255, 255))
            h += h
        return img
        
    @classmethod
    async def create_image(cls, team, matchdata, bans):
        offset = 68
        height = 1080
        width = 1920
        color = (14, 34, 43)
        img = Image.new('RGBA', (width, height), color=color)
        i = 0
        offset2 = 0
        items = []
        while i < 5:
            champ_icon = await helper2.get_champ_icon(team[2])
            champ_icon = Image.open(champ_icon)
            champ_icon = champ_icon.resize((280, 280))
            img.paste(champ_icon, (10, 10))
            items.append(team[0])
            player_key = await helper2.player_key(items)
            img.paste(player_key, (offset + offset2, offset))
            offset2 += 300 + offset
            i += 1
        
        # Final image product
        final_buffer = BytesIO()
        # Store the pillow image we just created into the buffer with the PNG format
        img.save(final_buffer, "PNG")
        # seek back to the start of the buffer stream
        final_buffer.seek(0)
        return final_buffer