import discord
from redbot.core import commands

from .taskhelper import TaskHelper

class GiveAway(TaskHelper, commands.Cog):
    def __init__(self):
        TaskHelper.__init__(self)
        self.conf = Config.get_conf(self, 975667633)
        defaults = { "channel": 0, "msg": 0 }
        self.conf.register_guild(**defaults)