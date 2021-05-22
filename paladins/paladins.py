import arez
from redbot.core import checks, commands
import asyncio
import humanize
from datetime import datetime
import discord
from .helper import helper
from redbot.core.utils.chat_formatting import pagify, text_to_file
import aiohttp
import json
import math
from tabulate import tabulate
from collections import Counter

class Paladins(commands.Cog):
    """Paladins stats cog by Mucski
    For a better experience you should link yout discord account to hirez
    that way you can use most commands without typing anything else but the command itself

    example: [p]champstats
    """
    def __init__(self, bot):
        self.bot = bot
        self.f = open("/home/ubuntu/key.txt", "r")
        self.auth = self.f.readline()
        self.devid = self.f.readline()
        self.api = arez.PaladinsAPI(dev_id=self.devid.strip(),
                                    auth_key=self.auth.strip())

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
        await ctx.bot.on_command_error(ctx, error, unhandled_by_cog=True)

    @commands.command()
    async def match(self, ctx, matchid: int):
        """Returns a match played from a given ID.
        This command only supports integer. 
        For player names use [p]last (player) (platform) 
        See [p]help last for more info.
        """
        async with ctx.typing():
            match = await self.api.get_match(matchid, expand_players=True)
            team1_data = []
            team2_data = []
            team1_champs = []
            team1_ranks = []
            team2_ranks = []
            team2_champs = []
            match_info = [match.id, match.duration.minutes, match.region.name,
                          match.map_name, match.score[0], match.score[1]]
            temp = match.bans
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
                    team1_champs.append(match_player.champion.name)
                    team1_ranks.append(rank)
                else:
                    if match_player.player.private:
                        rank = "99"
                    else:
                        rank = match_player.player.ranked_best.rank.value
                    team2_data.append(row)
                    team2_champs.append(match_player.champion.name)
                    team2_ranks.append(rank)
            buffer = await helper.historyimg(team1_champs, team2_champs, team1_data, team2_data, team1_ranks,
                                                team2_ranks, (match_info + temp))
            file = discord.File(filename=f"{matchid}.png", fp=buffer)
        await ctx.send(file=file)
        
    @commands.command()
    @checks.is_owner()
    async def proto(self, ctx):
        async with ctx.typing():
            team1_data = []
            team2_data = []
            team1_champs = []
            team1_ranks = []
            team2_ranks = []
            team2_champs = []
            cunt = 0
            match_info = ["198372984", "30", "Japan",
                          "Timber Mill", "1", "4"]
            temp = ["Makoa", "Yagorath", "Furia", "Jenos"]
            while cunt < 10:
                cunt += 1
                row = [
                        "TestSomeLongName", "999", "9999", "99/99/99",
                        "999999", "999999", "999", "999999",
                        "999999", "4", "Steam", "999999",
                        99.99
                ]
                if cunt < 6:
                    rank = "22"
                    team1_data.append(row)
                    team1_champs.append("Octavia")
                    team1_ranks.append(rank)
                else:
                    rank = "22"
                    team2_data.append(row)
                    team2_champs.append("Sha Lin")
                    team2_ranks.append(rank)
            buffer = await helper.historyimg(team1_champs, team2_champs, team1_data, team2_data, team1_ranks,
                                                team2_ranks, (match_info + temp))
            file = discord.File(filename=f"prototype.png", fp=buffer)
        await ctx.send(file=file)
            
    @commands.command()
    async def last(self, ctx, player = None, platform="PC"):
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
            temp = match.bans
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
                    team1_champs.append(match_player.champion.name)
                    team1_ranks.append(rank)
                else:
                    if match_player.player.private:
                        rank = "99"
                    else:
                        rank = match_player.player.ranked_best.rank.value
                    team2_data.append(row)
                    team2_champs.append(match_player.champion.name)
                    team2_ranks.append(rank)
            buffer = await helper.historyimg(team1_champs, team2_champs, team1_data, team2_data, team1_ranks,
                                                team2_ranks, (match_info + temp))
            file = discord.File(filename=f"{player}.png", fp=buffer)
        await ctx.send(file=file)

    @commands.command()
    @checks.is_owner()
    async def hirez(self, ctx, request, *msg):
        try:
            data = await self.api.request(request, *msg)
        except arez.HTTPException as exc:
            exc = exc.cause
            if isinstance(exc, aiohttp.ClientResponseError):
                await ctx.send(f"```\n{exc.status}: {exc.message}\n```")
                return
            elif isinstance(exc, aiohttp.ClientConnectionError):
                await ctx.send(f"```\nFailed to connect to api.\n```")
                return
            elif isinstance(exc, asyncio.TimeoutError):
                await ctx.send("```\nTimed out.\n```")
                return
            else:
                await ctx.send("```\nUnknown error\n```")
                return
        response = json.dumps(data, indent=4, sort_keys=True)
        if len(response) > 2000:
            file = text_to_file(response, "output.txt")
            await ctx.send(file=file)
        else:
            await ctx.send("```json\n" + response + "```")
            
    @commands.command()
    async def history(self, ctx, player = None, platform = "PC"):
        """Returns the history of someone (or yourself)
        Usage: [p]history name platform (or leave both blank for yourself if you have discord linked to hirez)
        """
        async with ctx.typing():
            if player is None:
                discord_id = ctx.author.id
                try:
                    ret = await self.api.get_from_platform(discord_id, arez.Platform.Discord)
                    ret = await ret
                except arez.NotFound:
                    await ctx.send("```\nDiscord account not linked to HiRez. Please link it first\n```")
                    return
            else:
                ret = await self.api.search_players(player, arez.Platform(platform))
                ret = await ret[0]
            history = await ret.get_match_history()
            if not history:
                await ctx.send("Player did not play for over a month. Nothing to display.")
                return
            table = []
            final_kda = 0
            kda_counter = 0
            for match in history:
                t = []
                if match.winner:
                    t.append("+")
                else:
                    t.append("-")
                t.append(match.id)
                t.append(match.map_name)
                t.append(match.champion.name)
                t.append(match.kda_text)
                t.append("{:.2f}".format(match.kda2))
                final_kda += match.kda2
                kda_counter += 1
                table.append(t)
            table_done = tabulate(table, headers = ["#", "Match ID", "Map", "Champion", "KDA", "KDA2"], tablefmt = "presto")
            champs = Counter(m.champion for m in history)
            most_champ = champs.most_common(1)[0][0].name
            if all(isinstance(c, arez.Champion) for c in champs.keys()):
                classes = Counter(m.champion.role for m in history)
                most_class = classes.most_common(1)[0][0]
            else:
                most_class = "Unknown"
            for page in pagify(table_done):
                await ctx.send("```dif\n{}\n```".format(page))
            await ctx.send("```\nMost played champion: {}\nMost played class: {}\nAverage KDA: {:.2f}\n```".format(most_champ, most_class, final_kda / kda_counter))
        
    @commands.command()
    async def champstats(self, ctx, champion_name = "all", player = None, platform = "PC"):
        """Returns champion stats, individual or multiple
        [p]champstats wr name platform to sort by winrate
        [p]champstats kda name platform to sort by kda
        [p]champstats all name platform sorts by level by default
        [p]champstats champion for individual
        """
        async with ctx.typing():
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
                
    @commands.command()
    async def current(self, ctx, name = None, platform = "PC"):
        """Returns the current match for yourself or someone.
        [p]help current for more information
        [p]current player platform or leave blank for yourself if you have discoed linked to hirez
        """
        async with ctx.typing():
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
                    t.append(f"???")
                    team1.append(t)
                else:
                    t = []
                    t.append(i)
                    t.append(f"{live_player.player.name}({live_player.account_level})")
                    t.append(f"{live_player.champion.name}({live_player.mastery_level})")
                    t.append(f"({live_player.player.casual.winrate_text})")
                    team1.append(t)
            for i, live_player in enumerate(live_match.team2, 1):
                if live_player.player.private:
                    t = []
                    t.append(i)
                    t.append(f"?????({live_player.account_level})")
                    t.append(f"{live_player.champion.name}({live_player.mastery_level})")
                    t.append(f"???")
                    team2.append(t)
                else:
                    t = []
                    t.append(i)
                    t.append(f"{live_player.player.name}({live_player.account_level})")
                    t.append(f"{live_player.champion.name}({live_player.mastery_level})")
                    t.append(f"({live_player.player.casual.winrate_text})")
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
    async def stats(self, ctx, name = None, platform="PC"):
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
    async def friends(self, ctx, name = None, platform="PC"):
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
        friends = await player.get_friends()
        file = text_to_file(''.join(friends), "test.txt")
        await ctx.send(file=file)
