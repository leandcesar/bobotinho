# -*- coding: utf-8 -*-
from tortoise import Tortoise


class Database:
    def __init__(self, url: str):
        self.__url = url
        self.__modules = {"models": ["bobotinho.database.models"]}

    async def init(self):
        await Tortoise.init(db_url=self.__url, modules=self.__modules)
        await Tortoise.generate_schemas(safe=True)

    async def close(self):
        await Tortoise.close_connections()
