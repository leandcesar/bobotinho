# -*- coding: utf-8 -*-
from bobotinho.logger import log


async def send_message(bot, channel: str, response: str) -> None:
    try:
        if not bot.channels[channel]["status"]:
            return
        if any(x in response for x in bot.channels[channel]["banwords"]):
            return
        await bot.get_channel(channel).send(response)
        log.info(f"#{channel} @{bot.nick}: {response}")
    except Exception as e:
        log.exception(e)
