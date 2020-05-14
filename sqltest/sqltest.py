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
        guild_id TEXT,
        msg TEXT,
        channel_id TEXT,
        )
        """)
        
    @commands.group(invoke_without_command=True)
    async def test(self, ctx):
        