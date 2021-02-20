import os

from dotenv import load_dotenv
from discord.ext import commands

# try:
#     load_dotenv(dotenv_path="secrets.env")
# except:
#     pass

DISCORD_API_KEY = os.getenv("DISCORD_API")

bot = commands.Bot(command_prefix=os.getenv("COMMAND_PREFIX"))

initial_extensions = ['cogs.command_error_handler',
                      'cogs.commands']


if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)

        except Exception as e:
            print(e)
            print(f'Failed to load extension "{extension}"')

    bot.run(DISCORD_API_KEY, bot=True, reconnect=True)
