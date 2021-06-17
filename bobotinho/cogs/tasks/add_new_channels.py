# -*- coding: utf-8 -*-
import asyncio

from bobotinho.cogs.tasks import send_message
from bobotinho.database import models


async def func(bot):
    # TODO: substituir por trigger
    last = await models.Channel.filter().order_by("-id").first()
    last_id = last.id if last else 0
    while True:
        channel = await models.Channel.get_or_none(id=last_id+1)
        if not channel:
            await asyncio.sleep(60, loop=bot.loop)
            continue
        last_id = channel.id
        await channel.fetch_related("user")
        if channel.user.name in bot.channels:
            continue
        await bot.join_channels([channel.user.name])
        bot.channels[channel.user.name] = {
            "banwords": list(channel.banwords.keys()),
            "disabled": list(channel.disabled.keys()),
            "status": channel.status,
        }
        response = (
            f'@{channel.user.name}, meu prefixo é "{bot.prefixes[0]}", '
            f'experimente enviando "{bot.prefixes[0]}help"'
        )
        await send_message(bot, channel.user.name, response)
