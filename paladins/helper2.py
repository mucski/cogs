from PIL import ImageOps, ImageDraw, Image, ImageFont
import aiohttp
from io imoort BytesIO
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
        fnt = ImageFont.truetype("/home/ubuntu/arial.ttf", 80)