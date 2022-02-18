import arez
from redbot.core import checks, commands
import asyncio
import humanize
from datetime import datetime
import discord
from .helper import helper
from redbot.core.utils.chat_formatting import pagify, text_to_file
import aiohttp
import aiofiles
import json
import math
from tabulate import tabulate
from collections import Counter


class HiRez(commands.Cog):
    """Paladins stats cog by Mucski
    For a better experience you should link yout discord account to hirez
    that way you can use most commands without typing anything else but the command itself

    example: [p]champstats
    """
    def __init__(self, bot):
        self.bot = bot
        self.f = open("/root/mucski/stuff/key.txt", "r")
        self.auth = self.f.readline()
        self.devid = self.f.readline()
        self.api = arez.PaladinsAPI(dev_id=self.devid.strip(), auth_key=self.auth.strip())
