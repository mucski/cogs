import discord
import math
from redbot.core.utils.chat_formatting import bold, box, humanize_list, humanize_number, pagify, humanize_timedelta
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS


class Main:
    async def leaderboard(self, ctx):
        userinfo = await self.conf.all_users()
        if not userinfo:
            return await ctx.send(bold("Start playing first, then check boards."))
        sorted_acc = sorted(userinfo.items(), key=lambda x: x[1]['cookies'], reverse=True)[:50]
        li = []
        for i, (user_id, account) in enumerate(sorted_acc, start=1):
            user_obj = ctx.guild.get_member(user_id)
            if len(user_obj.display_name) < 13:
                li.append(f"#{i:2}. {user_obj.display_name:<13} {account['cookies']:>15} 🍪")
            else:
                li.append(f"#{i:2}. {user_obj.display_name[:10]:<10}... {account['cookies']:>15} 🍪")
        text = "\n".join(li)
        page_list=[]
        for page_num, page in enumerate(pagify(text, delims=['\n'], page_length=1000), start=1):
            embed=discord.Embed(
                description=box(f"Cookieboards", lang="prolog") + (box(page, lang="md")),
            )
            embed.set_footer (
                text=f"Page {page_num}/{math.ceil(len(text) / 1000)}",
            )
        page_list.append(embed)
        return await menu(ctx, page_list, DEFAULT_CONTROLS)

    async def profile(self, ctx, member):
        """ Checks your balance or some ones """
        if member is None:
            member = ctx.author
        cookie = await self.cv(member)
        now = datetime.utcnow().replace(microsecond=0)
        daily_stamp = await self.conf.user(member).daily_stamp()
        daily_stamp = datetime.fromtimestamp(daily_stamp)
        remaining = daily_stamp - now
        #build embed
        e = discord.Embed(color=await self.color(ctx), timestamp=datetime.utcnow())
        e.set_author(name=f"Profile for {member.name}", icon_url=member.avatar_url)
        e.set_thumbnail(url=member.avatar_url)
        e.add_field(name="Cookies owned", value=f"``{cookie}``")
        if now < daily_stamp:
            cooling = "Yes"
            e.add_field(name="Daily on cooldown", value=f"``{cooling}``")
            e.add_field(name="Cooldown remaining", value=f"``{humanize_timedelta(timedelta=remaining)}``")
        else:
            cooling = "No"
            e.add_field(name="Daily on cooldown", value=f"``{cooling}``")
        await ctx.send(embed=e)
        