import discord
from redbot.core import commands
import sqlite3

class Sqltest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        db = sqlite3.connect("test.db")
        cursor = db.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS main(
        guild_id INT,
        msg_id INT,
        channel_id INT,
        user_id INT,
        )
        """)
        
    @commands.group(invoke_without_command=True)
    async def test(self, ctx):
        msg = await ctx.send("Hi")
        cursor.execute("SELECT * FROM main WHERE user_id=?", (ctx.author.id,))
        resp = cursor.fetchone()
        if not resp:
            cursor.execute("INSERT INTO main VALUES (?,?,?)",
                (ctx.guild.id, msg.id, ctx.channel.id,))
            db.commit()
            
        guildid, msgid, channelid = resp
        await ctx.send("{} {} {}".format(guildid, msgid, channelid))