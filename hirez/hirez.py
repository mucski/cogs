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

class HiRez(commands.Cog):
    """Paladins stats cog by Mucski
    For a better experience you should link yout discord account to hirez
    that way you can use most commands without typing anything else but the command itself

    example: [p]champstats
    """
    def __init__(self, bot):
        self.bot = bot
        self.f = open("/home/poopski/mucski/stuff/key.txt", "r")
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
                await ctx.send("```\nRequested profile is set to private.\n```")
                return
            if isinstance(exc, arez.NotFound):
                await ctx.send("```\nNot found!\n```")
                return
            if isinstance(exc, aiohttp.ClientResponseError):
                await ctx.send("```\nTimed out. Please try again in a minute.\n```")
            if isinstance(exc, arez.exceptions.HTTPException):
                await ctx.send("```\nSomething went wrong with the API. If the problem persists please contact Mucski.\n```")
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
                        f = await aiofiles.open(f'/home/poopski/mucski/stuff/icons/avatars/{name}.jpg', mode='wb')
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
            f"```\nAccount level: {player.calculated_level}\n"
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
        """
        Returns the current status of a player
        If he/she is in a match it will display their current match including players and ranks.
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
                await ctx.send("```\n{} is currently {}\n```".format(player, status.status))
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
            if champion_name.lower() == "betty" or champion_name.lower() == "bomba":
                champion_name = "Betty La Bomba"
            elif champion_name.lower() == "bk" or champion_name.lower() == "bombking" or champion_name.lower() == "bomb":
                champion_name = "Bomb King"
            elif champion_name.lower() == "sha" or champion_name.lower() == "shalin":
                champion_name = "Sha Lin"
            entry = await self.api.get_champion_info()
            champ = entry.champions.get(champion_name)
            if champ is None:
                await ctx.send("```\nInvalid champion name. Usage [p]chammpstats CHAMPION PLAYER PLATFORM(optional)!\n```")
                return
            stats = stats_dict.get(champ)
            if stats is None:
                await ctx.send("```\n{} does not own this champion or did not play it yet.\n```".format(player))
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
    async def match(self, ctx, matchid: int):
        """Returns a match played from a given ID.
        This command only supports integer.
        For player names use [p]last (player) (platform)
        See [p]help last for more info.
        """
        async with ctx.typing():
            match = await self.api.get_match(matchid, expand_players=True)
            pic = helper.format_match(match)
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
                    await ctx.send("```\nDid not find anyone called {}\n```".format(player))
                    return
                player = player_list[0]
            match_list = await player.get_match_history()
            if not match_list:
                await ctx.send("```\nNo recent matches found. (History is only kept for 30 days)\n```")
                return
            match = await match_list[0]
            await match.expand_players()
            pic = helper.format_match(match)
            file = discord.File(filename=f"{player}.png", fp=pic)
            await ctx.send(file=file)
            # await ctx.send(match.bans)

    @commands.command()
    async def history(self, ctx, player=None, sorting=None, platform="PC"):
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
            if sorting == "ranked":
                filter_func = lambda m: m.queue.is_ranked()
            elif sorting == "casual":
                filter_func = lambda m: m.queue.is_casual()
            else:
                filter_func = None  # no filter
            for match in filter(filter_func , history):
                t = []
                if match.winner:
                    win = "+"
                else:
                    win = "-"
                t.append(win + match.map_name)
                t.append(match.champion.name)
                t.append(match.kda_text)
                t.append(match.id)
                if match.queue.is_ranked():
                    t.append("Ranked")
                elif match.queue.is_casual():
                    t.append("Casual")
                final_kda += match.kda2
                kda_counter += 1
                table.append(t)
            table_done = tabulate(table, tablefmt="plain", headers=["Map", "Champion", "KDA", "ID", "Type"])
            champs = Counter(m.champion for m in history)
            most_champ = champs.most_common(1)[0][0].name
            if all(isinstance(c, arez.Champion) for c in champs.keys()):
                classes = Counter(m.champion.role for m in history)
                most_class = classes.most_common(1)[0][0]
            else:
                most_class = "Unknown"
            for page in pagify(table_done, page_length=1900):
                await ctx.send("```diff\n{}\n```".format(page))
            if kda_counter:
                await ctx.send("```\nMost played champion: {}\nMost played class: {}\nAverage KDA: {:.2f}\n```".format(most_champ, most_class, final_kda / kda_counter))
            else:
                pass

    @commands.command()
    async def playercard(self, ctx, name=None, platform="PC"):
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
            if status.status == 5 or status.status == 0:
                player_status = "Last login: {}".format(humanize.naturaltime(datetime.utcnow() - player.last_login))
            else:
                player_status = "Currently: {}".format(status.status)
            playercard = await helper.generatecard(player)
            file = discord.File(filename=f"{player.name}.png", fp=playercard)
            await ctx.send(file=file)

    @commands.command()
    async def globalkda(self, ctx, playerid: int):
        resp = await helper.get_kda_guru(playerid)
        if resp:
            await ctx.send("Your global KDA according to Paladins.guru is {}".format(resp[3]))
        else:
            await ctx.send("No response returned.")
