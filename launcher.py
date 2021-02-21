import os
import asyncio

from dotenv import load_dotenv
from discord.ext import commands
import aiohttp
from aiohttp import web

from cogs.http_endpoints import routes


if not os.getenv("DISCORD_API"):
    load_dotenv(dotenv_path="secrets.env")

HTTP_SERVER_PORT = os.getenv("HTTP_SERVER_PORT")
DISCORD_API_KEY = os.getenv("DISCORD_API")

bot = commands.Bot(command_prefix=os.getenv("COMMAND_PREFIX"))

initial_extensions = ['cogs.command_error_handler',
                      'cogs.commands']


async def run_http_server():
    app = web.Application()
    app.add_routes(routes)
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner, port=HTTP_SERVER_PORT)
    await site.start()
    print(f"HTTP server running on: {'0.0.0.0' if not site._host else site._host}:{site._port} ")


@bot.event
async def on_ready():
    print(f"Running: '{bot.user.name}', prefix '{os.getenv('COMMAND_PREFIX')}'")


if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)

        except Exception as e:
            print(e)
            print(f'Failed to load extension "{extension}"')

    asyncio.get_event_loop().run_until_complete(run_http_server())
    bot.run(DISCORD_API_KEY, bot=True, reconnect=True)
