# -*- coding: utf-8 -*-
from aiohttp.web import Application, Response, _run_app, get

import bobotinho


async def root(request):
    return Response(text=f"{bobotinho.__title__} v{bobotinho.__version__}")


async def func(bot):
    app = Application()
    app.add_routes([get("/", root)])
    await _run_app(app)
