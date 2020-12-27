from redbot.core import commands
import random
from discord import File

from PIL import Image, ImageDraw, ImageFont
import io

class Test2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test2(self, ctx):
        text = "Hello I am a test text"
        image = ""
        
    @commands.command()
    async def canvas(self, ctx, text=None):
    
        IMAGE_WIDTH = 600
        IMAGE_HEIGHT = 300
    
        # create empty image 600x300 
        image = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT)) # RGB, RGBA (with alpha), L (grayscale), 1 (black & white)
    
        # or load existing image
        #image = Image.open('/home/furas/images/lenna.png')
    
        # create object for drawing
        draw = ImageDraw.Draw(image)
    
        # draw red rectangle with green outline from point (50,50) to point (550,250) #(600-50, 300-50)
        draw.rectangle([50, 50, IMAGE_WIDTH-50, IMAGE_HEIGHT-50], fill=(255,0,0), outline=(0,255,0))
    
        # draw text in center
        text = f'Hello {ctx.author.name}'

        font = ImageFont.truetype('Arial.ttf', 30)
    
        text_width, text_height = draw.textsize(text, font=font)
        x = (IMAGE_WIDTH - text_width)//2
        y = (IMAGE_HEIGHT - text_height)//2
    
        draw.text( (x, y), text, fill=(0,0,255), font=font)
    
        # create buffer
        buffer = io.BytesIO()
    
        # save PNG in buffer
        image.save(buffer, format='PNG')    
    
        # move to beginning of buffer so `send()` it will read from beginning
        buffer.seek(0) 
    
        # send image
        await ctx.send(file=File(buffer, 'myimage.png'))