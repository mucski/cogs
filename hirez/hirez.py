import arez
from redbot.core import checks, commands
import asyncio
import humanize
from datetime import datetime
import discord
from redbot.core.utils.chat_formatting import pagify, text_to_file, humanize_number
import aiohttp
import aiofiles
import json
import math
from tabulate import tabulate
from collections import Counter
from . import helper
import types
from PIL import ImageOps, ImageDraw, Image, ImageFont, ImageEnhance
from io import BytesIO

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

    def cog_unload(self):
        asyncio.createTask(self.api.close())
        self.f.close()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            exc = error.original
            if isinstance(exc, arez.Unavailable):
                await ctx.send("```\nHiRez API is unavailable.\n```")
                return
            if isinstance(exc, arez.Private):
                await ctx.send("```\nRequested profile is set to private\n```")
                return
            if isinstance(exc, arez.NotFound):
                await ctx.send("```\nNot found!\n```")
                return
            if isinstance(exc, aiohttp.ClientResponseError):
                await ctx.send("```\nTimed out. Try again in a minute\n```")
            if isinstance(exc, arez.exceptions.HTTPException):
                await ctx.send("```\nSomething went wrong, try again with another user/id/name or try agian later\n```")
        await ctx.bot.on_command_error(ctx, error, unhandled_by_cog=True)

    @commands.command()
    async def status(self, ctx):
        """Paladins server statuses
        Green means online, red means offline, yellow means limited access
        """
        status = await self.api.get_server_status()
        stringus = ""
        for k, v in status.statuses.items():
            if v.status == "Operational":
                server = "🟢"
            elif v.status == "Limited Access":
                server = "🟡"
            else:
                server = "🔴"
            desc = (
                "```\n"
                f"Platform: {v.platform}\n"
                f"Status: {server} {v.status}\n"
                f"Version: {v.version}\n\n"
                "```"
            )
            stringus += desc
        e = discord.Embed(title="Paladins Server Status", color=await self.bot.get_embed_color(ctx), description=stringus)
        e.set_footer(text=f"Current time: {status.timestamp.strftime('%c')}")
        await ctx.send(embed=e)

    @commands.command()
    @checks.is_owner()
    async def downloadchamps(self, ctx):
        """
        This downloads all the champion avatars into the folder specified bellow
        """
        entry = await self.api.get_champion_info()
        for champ in entry.champions:
            async with aiohttp.ClientSession() as session:
                url = champ.icon_url
                name = champ.name.lower().replace(" ","-").replace("'","")
                async with session.get(url) as resp:
                    if resp.status == 200:
                        f = await aiofiles.open(f'root/mucski/stuff/icons/avatars/{name}.jpg', mode='wb')
                        await f.write(await resp.read())
                        await f.close()
        await ctx.tick()

    @commands.command()
    async def stats(self, ctx, name=None, platform="PC"):
        """Returns a players stats.
        [p]stats none or [p]stats (player) (platform)
        """
        if name is None:
            # use the ID of the caller
            discord_id = ctx.author.id
            try:
                player = await self.api.get_from_platform(discord_id, arez.Platform.Discord)
                player = await player
            except arez.NotFound:
                await ctx.send("```\nDiscord account not linked to HiRez. Please link it first\n```")
                return
        else:
            # player is a str here
            player_list = await self.api.search_players(name, arez.Platform(platform))
            player = await player_list[0]
        status = await player.get_status()
        if status.status == 5 or status.status == 0:
            player_status = "Last login: {}".format(humanize.naturaltime(datetime.utcnow() - player.last_login))
        else:
            player_status = "Currently: {}".format(status.status)
        desc = (
            "**__Player Stats__**\n"
            f"```\nAccount level: {player.level}\n"
            f"Playtime: {math.floor(player.playtime.total_hours())} hours\n"
            f"Region: {player.region}\n"
            f"Champions Owned: {player.champion_count}\n"
            f"Achievements Unlocked: {player.total_achievements}\n"
            "Account Created: "
            f"{humanize.naturaltime(datetime.utcnow() - player.created_at)}\n"
            f"{player_status}"
            "\n```"
            "**__Casual Stats__**\n"
            "```\nWin Rate: "
            f"{player.casual.wins}/{player.casual.losses}"
            f" ({player.casual.winrate_text})\n"
            f"Deserted: {player.casual.leaves}\n```"
            f"**__Ranked Stats Season {player.ranked_best.season}__**\n"
            f"```\nWin Rate: "
            f"{player.ranked_best.wins}/{player.ranked_best.losses}"
            f" ({player.ranked_best.winrate_text})\n"
            f"Deserted: {player.ranked_best.leaves}\n"
            f"Ranked Type: {player.ranked_best.type}\n"
            f"Current Rank: {player.ranked_best.rank}"
            f" ({player.ranked_best.points} TP)\n```"
        )
        if status.status == 5 or status.status == 0:
            status_emoji = "🔴"
        else:
            status_emoji = "🟢"
        e = discord.Embed(color=await self.bot.get_embed_color(ctx),
                          title=f"{status_emoji} {player.name} ({player.platform}) "
                                f"_({player.title})_")
        e.description = desc
        e.set_thumbnail(url=player.avatar_url)
        e.set_footer(text=f"Player ID: {player.id}")
        await ctx.send(embed=e)

    @commands.command()
    async def current(self, ctx, name=None, platform="PC"):
        """Returns the current match for yourself or someone.
        [p]help current for more information
        [p]current player platform or leave blank for yourself if you have discoed linked to hirez
        """
        # async with ctx.typing():
        if name is None:
            # use the ID of the caller
            discord_id = ctx.author.id
            try:
                player = await self.api.get_from_platform(discord_id, arez.Platform.Discord)
                player = await player
            except arez.NotFound:
                await ctx.send("```\nDiscord account not linked to HiRez. Please link it first\n```")
                return
        else:
            # player is a str here
            player_list = await self.api.search_players(name, arez.Platform(platform))
            player = await player_list[0]
        status = await player.get_status()
        live_match = await status.get_live_match()
        if not live_match:
            await ctx.send("```\n{} is currently not in a match or unsupported queue (customs)\n```".format(player))
            return
        await live_match.expand_players()
        team1 = []
        team2 = []
        for i, live_player in enumerate(live_match.team1, 1):
            if live_player.player.private:
                t = []
                t.append(i)
                t.append(f"?????({live_player.account_level})")
                t.append(f"{live_player.champion.name}({live_player.mastery_level})")
                t.append("???")
                t.append(f"{live_player.rank}")
                team1.append(t)
            else:
                t = []
                t.append(i)
                t.append(f"{live_player.player.name}({live_player.account_level})")
                t.append(f"{live_player.champion.name}({live_player.mastery_level})")
                t.append(f"({live_player.player.casual.winrate_text})")
                t.append(f"{live_player.rank}")
                team1.append(t)
        for i, live_player in enumerate(live_match.team2, 1):
            if live_player.player.private:
                t = []
                t.append(i)
                t.append(f"?????({live_player.account_level})")
                t.append(f"{live_player.champion.name}({live_player.mastery_level})")
                t.append("???")
                t.append(f"{live_player.rank}")
                team2.append(t)
            else:
                t = []
                t.append(i)
                t.append(f"{live_player.player.name}({live_player.account_level})")
                t.append(f"{live_player.champion.name}({live_player.mastery_level})")
                t.append(f"({live_player.player.casual.winrate_text})")
                t.append(f"{live_player.rank}")
                team2.append(t)
        team1_done = tabulate(team1, tablefmt="plain")
        team2_done = tabulate(team2, tablefmt="plain")
        desc = (
            f"Map: {live_match.map_name}\n"
            f"Region: {live_match.region}\n"
            "```\n"
            f"{''.join(team1_done)}\n"
            "```"
            "Versus\n"
            "```\n"
            f"{''.join(team2_done)}\n"
            "```"
        )
        e = discord.Embed(color=await self.bot.get_embed_color(ctx),
                            title=f"{player.name} is in a {live_match.queue}")
        e.description = desc
        e.set_thumbnail(url=player.avatar_url)
        e.set_footer(text=f"Match ID: {live_match.id} / Missing players are bots.")
        await ctx.send(embed=e)

    @commands.command()
    async def champstats(self, ctx, champion_name="all", player=None, platform="PC"):
        """Returns champion stats, individual or multiple
        [p]champstats wr name platform to sort by winrate
        [p]champstats kda name platform to sort by kda
        [p]champstats all name platform sorts by level by default
        [p]champstats champion for individual

        for champions with spaces do it like "sha lin"
        """
        # async with ctx.typing():
        if player is None:
            # use the ID of the caller
            discord_id = ctx.author.id
            try:
                ret = await self.api.get_from_platform(discord_id, arez.Platform.Discord)
                ret = await ret
            except arez.NotFound:
                await ctx.send("```\nDiscord account not linked to HiRez. Please link it first\n```")
                return
        else:
            # player is a str here
            ret = await self.api.search_players(player, arez.Platform(platform))
            ret = await ret[0]
        champions_stats = await ret.get_champion_stats()
        stats_dict = {s.champion: s for s in champions_stats}  # Dict[Champion, ChampionStats]
        if champion_name == "all" or champion_name == "kda" or champion_name == "wr":
            table = []
            hours_count = 0
            if champion_name == "kda":
                key = lambda s: s.kda2
            elif champion_name == "wr":
                key = lambda s: s.winrate_text
            else:
                key = lambda s: s.level
            for stats in sorted(champions_stats, key=key, reverse=True):
                t = []
                t.append(f"{stats.champion.name}({stats.level})")
                t.append("{:.2f}".format(stats.kda))
                t.append(f"{stats.winrate_text}")
                t.append(f"{math.floor(stats.playtime.total_hours())} h")
                hours_count += stats.playtime.total_hours()
                table.append(t)
            table_done = tabulate(table, headers=["Name(lvl)", "K/D/A", "Winrate", "Time"], tablefmt="presto")
            for page in pagify(table_done):
                await ctx.send("```\n{}\n```".format(page))
            await ctx.send("```\nTotal Hours: {}\n```".format(int(hours_count)))
        else:
            entry = await self.api.get_champion_info()
            champ = entry.champions.get(champion_name)
            if champ is None:
                await ctx.send("```\nYou dun fucked up the champ's name!\n```")
                return
            stats = stats_dict.get(champ)
            if stats is None:
                await ctx.send("```\nYou ain't played this champ yet!\n```")
                return
            desc = (
                f"```\nChampion role: {champ.role}\n"
                f"Champion level: {stats.level}\n"
                "Champion KDA: {:.2f}".format(stats.kda) + "\n"
                f"Winrate: {stats.kda_text} ({stats.winrate_text})\n"
                f"Matches played: {stats.matches_played}\n"
                f"Playtime: {math.floor(stats.playtime.total_hours())} hours\n"
                f"Experience: {stats.experience}\n"
                f"Last played: {humanize.naturaltime(datetime.utcnow() - stats.last_played)}\n```"
            )
            e = discord.Embed(color=await self.bot.get_embed_color(ctx), title=f"{champ.name} ({champ.title})")
            e.set_thumbnail(url=champ.icon_url)
            e.description = desc
            e.set_footer(text=f"Individual champion stats for {ret.name}")
            await ctx.send(embed=e)

    def format_match(self, match: arez.Match) -> Image:
        W, H = (4620, 2932)
        # padding=10
        img = Image.new("RGB", (W, H), color=(8, 21, 25))
        # headers
        key = helper.playerkey(W, H)
        img.paste(key, (0, 0))
        # format in the players
        for team_num in range(1, 3):  # 1 then 2
            yoffset = (team_num - 1) * 1772  # replace 1000 with whatever offset you'll need
            team = getattr(match, f"team{team_num}")
            for i, mp in enumerate(team):
                y = i * 232 + yoffset  # replace 50 with whatever row height you use
                row = helper.statsimage(mp, i)  # your current playerkey
                img.paste(row, (0, 232 * i + y))
                # base.paste(row, 0, y)
        # add middlebar
        middle = helper.middlepanel(match)
        img.paste(middle, (0, int(H / 2 - 200)))
        #base.paste(middlebar(match))
        historyimg = img.resize((int(W / 2), int(H / 2)), Image.ANTIALIAS)
        final_buffer = BytesIO()
        historyimg.save(final_buffer, "PNG")
        final_buffer.seek(0)
        return final_buffer

    @commands.command()
    async def match(self, ctx, matchid: int):
        """Returns a match played from a given ID.
        This command only supports integer.
        For player names use [p]last (player) (platform)
        See [p]help last for more info.
        """
        async with ctx.typing():
            match = await self.api.get_match(matchid, expand_players=True)
            pic = await self.format_match(match)
            file = discord.File(filename="test.png", fp=pic)
            await ctx.send(file=file)

    @commands.command()
    async def last(self, ctx, player=None, platform="PC"):
        """Returns the last played match by player
        player can be a string or a discord member (mention)
        Platform is optional
        If you have Discord linked to HiRez, you can just type [p]last
        followed by nothing.
        """
        async with ctx.typing():
            if player is None:
                # use the ID of the caller
                discord_id = ctx.author.id
                try:
                    player = await self.api.get_from_platform(discord_id, arez.Platform.Discord)
                except arez.NotFound:
                    await ctx.send("```\nDiscord account not linked to HiRez. Please link it first\n```")
                    return
            else:
                # player is a str here
                try:
                    player_list = await self.api.search_players(player, arez.Platform(platform))
                except arez.NotFound:
                    await ctx.send("```\nNo players found with that name\n```")
                    return
                player = player_list[0]
            match_list = await player.get_match_history()
            if not match_list:
                await ctx.send("```\nNo recent matches found.\n```")
                return
            match = await match_list[0]
            await match.expand_players()
            team1_data = []
            team2_data = []
            team1_champs = []
            team1_ranks = []
            team2_ranks = []
            team2_champs = []
            match_info = [match.id, match.duration.minutes, match.region.name,
                            match.map_name, match.score[0], match.score[1]]
            bans = match.bans
            for match_player in sorted(match.players, key=lambda match_player: match_player.df, reverse=True):
                row = [
                        match_player.player.name, match_player.account_level, match_player.credits, match_player.kda_text,
                        match_player.damage_done, match_player.damage_taken, match_player.objective_time, match_player.damage_mitigated,
                        match_player.healing_done, match_player.party_number, match_player.player.platform, match_player.healing_self,
                        match_player.kda2
                ]
                if match_player.team_number == 1:
                    if match_player.player.private:
                        rank = "99"
                    else:
                        rank = match_player.player.ranked_best.rank.value
                    team1_data.append(row)
                    team1_champs.append(match_player.champion)
                    team1_ranks.append(rank)
                else:
                    if match_player.player.private:
                        rank = "99"
                    else:
                        rank = match_player.player.ranked_best.rank.value
                    team2_data.append(row)
                    team2_champs.append(match_player.champion.name)
                    team2_ranks.append(rank)
            buffer = await helper.historyimg(team1_champs, team2_champs, team1_data, team2_data, team1_ranks, team2_ranks, (match_info + bans))
            file = discord.File(filename=f"{player}.png", fp=buffer)
            await ctx.send(file=file)
