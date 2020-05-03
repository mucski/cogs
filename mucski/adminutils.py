import discord

class AdminUtils:
    
    def shuffle(self, word):
        word = list(word)
        random.shuffle(word)
        return ''.join(word)
        
    async def add_pet(self, ctx, pet, member):
        if member is None:
            member = ctx.author
        #todo: get pet name drom list asap
        await self.conf.user(member).pet.set(pet)
        return await ctx.send(f"Gave {pet} pet to {member.name}")
        
    async def remove_pet(self, ctx, member):
        await self.conf.user(member).pets.clear()
        return await ctx.send(f"Removed pet from {member.name}")
        
    async def add_cookie(self, ctx, amt: int, member):
        cookie = await self.conf.user(member).cookies()
        final = cookie + amt
        await self.conf.user(member).cookies.set(final)
        return await ctx.send(f"Added {amt} to {member.name} now has {cookie} cookies.")