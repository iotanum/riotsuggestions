from aiohttp import web


routes = web.RouteTableDef()


@routes.get('/get_picks')
async def response(request):
    return web.Response(text="Goodbyes, world")
