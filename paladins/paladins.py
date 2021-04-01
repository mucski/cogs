import arez
from redbot.core import checks, commands
import asyncio
import humanize
from datetime import datetime
import discord
from discord import File
from .helper import helper
from redbot.core.utils.chat_formatting import pagify
import aiohttp
import json
from io import StringIO


class Paladins(commands.Cog):
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
                await ctx.send("HiRez API is offline or unavaiable.")
                return
            if isinstance(exc, arez.Private):
                await ctx.send("Requested profile is set to private")
                return
            if isinstance(exc, arez.NotFound):
                await ctx.send("Player was not found")
                return
        await ctx.bot.on_command_error(ctx, error, unhandled_by_cog=True)

    @commands.command()
    async def match(self, ctx, match_id_name):
        async with ctx.typing():
            if match_id_name.isdecimal():
                match = await self.api.get_match(match_id_name, expand_players=True)
            else:
                match = await self.api.get_player(match_id_name)
                match = await match.get_match_history()
                try:
                    match = await match[0]
                except IndexError:
                    await ctx.send("No match found.")
                    return
                await match.expand_players()
            team1_data = []
            team2_data = []
            team1_champs = []
            team1_ranks = []
            team2_ranks = []
            team2_champs = []
            match_info = [match.winning_team, match.duration.minutes, match.region.name,
                          match.map_name, match.score[0], match.score[1]]
            temp = match.bans
            for match_player in match.players:
                if match_player.team_number == 1:
                    if match_player.player.private:
                        rank = "99"
                    else:
                        rank = match_player.player.ranked_best.rank.value
                    team1_data.append([match_player.player.name, match_player.account_level, match_player.credits, match_player.kda_text,
                                       match_player.damage_done, match_player.damage_taken,
                                       match_player.objective_time, match_player.damage_mitigated,
                                       match_player.healing_done, match_player.party_number, match_player.player.platform, match_player.healing_self])
                    team1_champs.append(match_player.champion.name)
                    team1_ranks.append(rank)
                else:
                    if match_player.player.private:
                        rank = "99"
                    else:
                        rank = match_player.player.ranked_best.rank.value
                    team2_data.append([match_player.player.name, match_player.account_level, match_player.credits, match_player.kda_text,
                                       match_player.damage_done, match_player.damage_taken,
                                       match_player.objective_time, match_player.damage_mitigated,
                                       match_player.healing_done, match_player.party_number, match_player.player.platform, match_player.healing_self])
                    team2_champs.append(match_player.champion.name)
                    team2_ranks.append(rank)
            buffer = await helper.history_image(team1_champs, team2_champs, team1_data, team2_data, team1_ranks,
                                                team2_ranks, (match_info + temp))
            file = discord.File(filename=f"{match_id_name}.png", fp=buffer)
        await ctx.send(file=file)

    @commands.command()
    @checks.is_owner()
    async def hirez(self, ctx, request, *msg):
        data = await self.api.request(request, *msg)
        pretty = json.dumps(data, indent=4, sort_keys=True)
        if len(pretty) > 2000:
            pretty = StringIO()
            # pretty.save(json_data, "TXT")
            pretty.seek(0)
            file = discord.File(filename="output.txt", fp=pretty)
            await ctx.send(file=file)
        else:
            await ctx.send("```json\n" + pretty + "```")

    @commands.command()
    @checks.is_owner()
    async def testing(self, ctx):
        status = await self.api.get_server_status()
        await ctx.send(status)

    @commands.command()
    async def stats(self, ctx, player, platform="PC"):
        platform = arez.Platform(platform)
        if player.isdecimal():
            player = await self.api.get_player(player)
        else:
            player_obj = await self.api.search_players(player, platform)
            player = await player_obj[0]
        desc = (
            "**__Player Stats__**\n"
            f"```Account level: {player.level}\n"
            f"Playtime: {int(player.playtime.total_hours())} hours\n"
            f"Region: {player.region}\n"
            f"Champions Owned: {player.champion_count}\n"
            f"Achievements Unlocked: {player.total_achievements}\n"
            f"Account Created: "
            f"{humanize.naturaltime(datetime.utcnow() - player.created_at)}\n"
            f"Last Login: "
            f"{humanize.naturaltime(datetime.utcnow() - player.last_login)}\n"
            "```\n\n"
            f"**__Casual Stats__**\n"
            f"```Win Rate: "
            f"{player.casual.wins}/{player.casual.losses}"
            f" ({player.casual.winrate_text})\n"
            f"Deserted: {player.casual.leaves}\n```"
            "\n\n"
            f"**__Ranked Stats Season {player.ranked_best.season}__**\n"
            f"```Win Rate: "
            f"{player.ranked_best.wins}/{player.ranked_best.losses}"
            f" ({player.ranked_best.winrate_text})\n"
            f"Deserted: {player.ranked_best.leaves}\n"
            f"Ranked Type: {player.ranked_best.type}\n"
            f"Current Rank: {player.ranked_best.rank}"
            f" ({player.ranked_best.points} TP)\n```"
        )
        e = discord.Embed(color=await self.bot.get_embed_color(ctx),
                          title=f"{player.name}({player.platform})"
                                f"_({player.title})_")
        e.description = desc
        e.set_thumbnail(url=player.avatar_url)
        e.set_footer(text=f"Player ID: {player.id}")
        await ctx.send(embed=e)
