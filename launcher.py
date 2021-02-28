import os

from dotenv import load_dotenv
from discord.ext import commands


if not os.getenv("DISCORD_API"):
    load_dotenv(dotenv_path="secrets.env")

DISCORD_API_KEY = os.getenv("DISCORD_API")

bot = commands.Bot(command_prefix=os.getenv("COMMAND_PREFIX"))

initial_extensions = ['cogs.command_error_handler',
                      'cogs.commands',
                      'cogs.http_endpoints',
                      'cogs.helpers.opgg_players']


@bot.event
async def on_ready():
    await bot.get_cog("Commands").update_registry()
    print(f"Running: '{bot.user.name}', prefix '{os.getenv('COMMAND_PREFIX')}'")


if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)

        except Exception as e:
            print(e)
            print(f'Failed to load extension "{extension}"')

    bot.run(DISCORD_API_KEY, bot=True, reconnect=True)
