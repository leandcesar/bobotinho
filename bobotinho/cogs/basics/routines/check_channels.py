# -*- coding: utf-8 -*-
from bobotinho import log

delta = 60


async def routine(bot) -> None:
    try:
        connected_channels = [channel.name for channel in bot.connected_channels]
        disconnected_channels = [channel for channel in bot.channels.keys() if channel not in connected_channels]
        await bot.join_channels(disconnected_channels)
    except Exception as e:
        log.exception(e, extra={"locals": locals()})
