# -*- coding: utf-8 -*-
from tortoise import Tortoise


async def init(database_url: str, *, models_path: str = "bobotinho.database.models") -> None:
    models = [models_path]
    await Tortoise.init(db_url=database_url, modules={"models": models})
    await Tortoise.generate_schemas(safe=True)


async def close() -> None:
    await Tortoise.close_connections()
