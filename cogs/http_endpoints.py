from aiohttp import web
from discord.ext import commands
import aiohttp
from aiohttp import web

import os
import json


HTTP_SERVER_PORT = os.getenv("HTTP_SERVER_PORT")


class HTTPServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def http_server(self):
        async def invoke_bot_command(r_body):
            registry = self.bot.get_cog("Commands").registry

            for client_id, params in registry.items():
                if r_body['hostname'] in params['hostname']:
                    client_tag = f'<@{client_id}>'
                    channel_id = int(params['channel_id'])
                    await self.bot.get_channel(channel_id).send(f"{client_tag}\n{r_body}")

        async def get_handler(request):
            return web.Response(text=f"{self.bot.user.name}")

        async def post_handler(request):
            body = json.loads(await request.text())
            await invoke_bot_command(body)
            return web.Response(status=200)

        app = web.Application()
        app.router.add_get("/get", get_handler)
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
