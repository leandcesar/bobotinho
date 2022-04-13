# -*- coding: utf-8 -*-
from tortoise import Tortoise, signals

from bobotinho.database.afk import Afk  # NOQA
from bobotinho.database.bug import Bug  # NOQA
from bobotinho.database.channel import Channel  # NOQA
from bobotinho.database.cookie import Cookie  # NOQA
from bobotinho.database.pet import Pet  # NOQA
from bobotinho.database.player import Player  # NOQA
from bobotinho.database.reminder import Reminder  # NOQA
from bobotinho.database.suggest import Suggest  # NOQA
from bobotinho.database.user import User  # NOQA
from bobotinho.database.wedding import Wedding  # NOQA
from bobotinho.database.listeners import *  # NOQA


async def init(database_url: str, *, models_path: str = "bobotinho.database") -> None:
    models = [models_path]
    await Tortoise.init(db_url=database_url, modules={"models": models})
    await Tortoise.generate_schemas(safe=True)


async def close() -> None:
    await Tortoise.close_connections()


@signals.post_save(User)
async def update_user_name(sender, instance, created, using_db, update_fields):
    if not created and update_fields and "name" in update_fields:
        await Cookie.filter(id=instance.id).update(name=instance.name)
        await Player.filter(id=instance.id).update(name=instance.name)
