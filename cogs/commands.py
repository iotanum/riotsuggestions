from discord.ext import commands
import discord
from .helpers.guess_role import pull_data, guess_role
from .helpers.map_id_to_name import map_to_name

import requests
from requests import get
import random
import os


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_registry_dir = '/data/bot_registry/registry'
        self.registry = {}

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

    async def update_registry(self):
        if not os.path.exists(self.bot_registry_dir):
            open(self.bot_registry_dir, 'w').close()

        with open(self.bot_registry_dir, 'r') as file:
            registry = file.readlines()

            if registry == '':
                self.registry = {}
                return

            for _ in registry:
                # In order of registry_params variable above
                registry_params = _.split(',')
                registry_params = [param.replace("\n", '') for param in registry_params]

                if len(registry_params) == 3:
                    self.registry[registry_params[0]] = {}
                    self.registry[registry_params[0]]['channel_id'] = registry_params[2]
                    self.registry[registry_params[0]]['hostname'] = registry_params[1]

            file.close()

    async def add_to_registry(self, ctx=None, hostname=None):
        user_id = str(ctx.message.author.id)
        channel_id = ctx.message.channel.id
        registry_params = [user_id, hostname, channel_id]
        param_string = ",".join(str(param) for param in registry_params)
        param_string = f"{param_string}\n"

        if user_id not in self.registry:
            print("bla", self.registry, user_id)
            with open(self.bot_registry_dir, 'a') as file:
                file.write(param_string)
                file.close()
        else:
            with open(self.bot_registry_dir, 'r+') as file:
                d = file.readlines()
                file.seek(0)
                for line in d:
                    if user_id not in line:
                        print("written")
                        file.write(line)

                file.truncate()
                file.write(param_string)
                file.close()

        # always call update after mutating
        await self.update_registry()

        return True

    @commands.command(name='ip')
    async def give_ip(self, ctx):
        ingas = 398128290042347526

        if ctx.message.author.id == ingas or await self.bot.is_owner(ctx.message.author):
            ip = get('https://api.ipify.org').text
            await ctx.message.author.send(f"{ip}")
        else:
            await ctx.send("?")

    @commands.command()
    async def add(self, ctx, hostname):
        added = await self.add_to_registry(ctx, hostname)

        if added:
            await ctx.message.add_reaction("\U00002705")

    @commands.command()
    async def get_registry(self, ctx):
        await ctx.send(f"```\n {self.registry} \n```")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        message_content = message.content.lower()
        if 'thanks' in message_content and 'tyler' in message_content:
            await message.channel.send(random.choice(await self.replies()))


def setup(bot):
    bot.add_cog(Commands(bot))
