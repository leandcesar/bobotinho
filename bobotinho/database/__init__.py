# -*- coding: utf-8 -*-
from tortoise import Tortoise


class Database:
    def __init__(self, url: str):
        self.url = url

    async def init(self):
        models = ["bobotinho.database.models"]
        await Tortoise.init(db_url=self.url, modules={"models": models})
        await Tortoise.generate_schemas(safe=True)

    async def close(self):
        await Tortoise.close_connections()
