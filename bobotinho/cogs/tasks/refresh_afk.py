# -*- coding: utf-8 -*-
import asyncio

from bobotinho.database import models


async def func(bot) -> None:
    while True:
        for afk in await models.Afk.filter(status=False).all():
            if afk.updated_ago.total_seconds() > 180:
                await afk.delete()
        await asyncio.sleep(60, loop=bot.loop)
