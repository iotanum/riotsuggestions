from discord.ext import commands
import discord
from .helpers.guess_role import pull_data, guess_role
from .helpers.map_id_to_name import map_to_name

import requests
from requests import get
import random

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def format_message_to_champ_list(self, message):
        message = message.strip("()")
        message = message.split(" : ")

        my_team = [int(x) for x in message[0].split(" ")]
        enemy_team = [int(x) for x in message[1].split(" ")]

        print(my_team, enemy_team)
        return my_team, enemy_team

    async def format_final_dictionary_for_request(self, roles, my_team=True):
        side = "1" if my_team else "2"

        for role in list(roles.keys()):
            roles[role.lower() + side] = roles.pop(role)

        return roles

    async def format_request_form(self, message):
        my_team, enemy_team = await self.format_message_to_champ_list(message)

        champion_roles = pull_data()
        my_roles = guess_role(champion_roles, my_team, friendly_team=True)
        enemy_roles = guess_role(champion_roles, enemy_team)

        my_roles = await self.format_final_dictionary_for_request(my_roles)
        enemy_roles = await self.format_final_dictionary_for_request(enemy_roles, my_team=False)

        return {**my_roles, **enemy_roles}

    async def do_request(self, message):
        url = "http://88.222.156.52:8080/matchup/whatDoIPlay"

        try:
            req = requests.post(url, data=message)

            return req.json()
        except requests.exceptions.ConnectionError:
            return []

    @commands.command(brief="Suggest most suited picks for you!")
    async def pick(self, ctx, *, args):
        final_request_form = await self.format_request_form(args)
        print(final_request_form)
        suggestion_response = await self.do_request(final_request_form)
        print(suggestion_response, "\n")

        for key, value in final_request_form.items():
            if value == 0:
                lane_for_suggestion = key[:-1]

        try:
            suggestion_1 = suggestion_response['matchups'][0]
            suggestion_2 = suggestion_response['matchups'][1]
            suggestion_3 = suggestion_response['matchups'][2]
        except:
            pass

        embed = discord.Embed(title=f"What should you play in *{lane_for_suggestion}*, huh?",
                              description=f"👏 Went 👏 through 👏 **{suggestion_response['totalRecords']}** 👏 matches 👏",
                              color=0xd62424)

        if len(suggestion_response['matchups']) == 0:
            embed.add_field(name=f"Whoopsie poopsie",
                            value=f"Looks like there's no suggestions up in this bitch >.<",
                            inline=True)

        if len(suggestion_response['matchups']) >= 1:
            embed.add_field(name=f"{map_to_name(suggestion_1['pick'])}",
                            value=f"💯 **{suggestion_1['winrate']}%**\n"
                                  f"📈 *{suggestion_1['totalGames']}* games",
                            inline=True)

        if len(suggestion_response['matchups']) >= 2:
            embed.add_field(name=f"{map_to_name(suggestion_2['pick'])}",
                            value=f"💯 **{suggestion_2['winrate']}%**\n"
                                  f"📈 *{suggestion_2['totalGames']}* games",
                            inline=True)

        if len(suggestion_response['matchups']) >= 3:
            embed.add_field(name=f"{map_to_name(suggestion_3['pick'])}",
                            value=f"💯 **{suggestion_3['winrate']}%**\n"
                                  f"📈 *{suggestion_3['totalGames']}* games",
                            inline=True)
        embed.set_footer(text="REMEMBER! Your team (left side) must be sorted!\n"
                              "TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY")

        print(final_request_form)
        await ctx.send(embed=embed)

    async def replies(self):
        return ["is k", "yo np", "k", "np"]

    @commands.command(name='ip')
    async def give_ip(self, ctx):
        ingas = 398128290042347526

        if await self.bot.is_owner(ctx.message.author):
            ip = get('https://api.ipify.org').text
            await ctx.message.author.send(f"{ip}")
        else:
            await ctx.send("?")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        message_content = message.content.lower()
        if 'thanks' in message_content and 'tyler' or 'ignas' in message_content:
            await message.channel.send(random.choice(await self.replies()))


def setup(bot):
    bot.add_cog(Commands(bot))
