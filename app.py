# -*- coding: utf-8 -*-
import os
from aiohttp.web import Application, Response, RouteTableDef, run_app

import bobotinho

routes = RouteTableDef()


@routes.get("/")
async def root(request):
    return Response(text=f"{bobotinho.__title__} v{bobotinho.__version__}")


if __name__ == "__main__":
    app = Application()
    app.add_routes(routes)
    run_app(app, host=os.getenv("HOST"), port=os.getenv("PORT"))
