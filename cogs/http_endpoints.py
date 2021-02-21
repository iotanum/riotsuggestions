from aiohttp import web
from discord.ext import commands
import aiohttp
from aiohttp import web

import os


HTTP_SERVER_PORT = os.getenv("HTTP_SERVER_PORT")


class HTTPServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def http_server(self):
        async def get_handler(request):
            return web.Response(text=f"{self.bot.user.name}")

        async def post_handler(request):
            body = await request.text()
            return web.Response(text=body)

        app = web.Application()
        # app.router.add_get("/get", get_handler)
        app.router.add_post("/get", post_handler)

        runner = aiohttp.web.AppRunner(app)
        await runner.setup()
        site = aiohttp.web.TCPSite(runner, port=HTTP_SERVER_PORT)
        await self.bot.wait_until_ready()
        await site.start()
        print(f"HTTP server running on: {'0.0.0.0' if not site._host else site._host}:{site._port} ")


def setup(bot):
    server = HTTPServer(bot)
    bot.add_cog(server)
    bot.loop.create_task(server.http_server())
