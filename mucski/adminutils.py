import discord
from redbot.core import commands, checks

class AdminUtils:
    
    def shuffle(self, word):
        word = list(word)
        random.shuffle(word)
        return ''.join(word)
        
    async def add_pet(self, ctx, pet, member: discord.Member=None):
        if member is None:
            member = ctx.author
        #todo: get pet name drom list asap
        await self.conf.user(member).pet.set(pet)
        await ctx.send(f"Gave {pet} pet to {member.name}")
        
    async def remove_pet(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        await self.conf.user(member).pets.clear()
        await ctx.send(f"Removed pet from {member.name}")
        
    async def add_cookie(self, ctx, amt: int, member: discord.Member=None):
        if member is None:
            member = ctx.author
        cookie = await self.conf.user(member).cookies()
        final = cookie + amt
        await self.conf.user(member).cookies.set(final)
        await ctx.send(f"Added {amt} to {member.name} now has {cookie} cookies."
    
    async def del_cookie(self, ctx, amt: int, member: discord.Member=None):
        if member is None:
            member = ctx.author
        cookie = await self.conf.user(member).cookies()
        final = cookie - amt
        await self.conf.user(member).cookies.set(final)
        await ctx.send(f"Removed {amt} from {member.name} now has {cookie}")

    async def reset_db(self, ctx):
        await self.conf.clear_all()
        await self.conf.clear_all_globals()
        await self.conf.clear_all_users()
        await ctx.send("Thanos snapped the database.")
        
    async def cleardb(self, ctx, *, stuff):
        await self.conf.clear_raw(stuff)
        await ctx.send("done")
    
    async def reset_cd(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        await self.conf.user(member).daily_stamp.clear()
        await self.conf.user(member).steal_stamp.clear()
        await self.conf.user(member).work_stamp.clear()
        await self.conf.user(member).pet_stamp.clear()
        await self.conf.user(member).pets.mission.clear()
        await ctx.send(f"All cooldowns have been reset for 1 turn for {member.name}")
        
    
