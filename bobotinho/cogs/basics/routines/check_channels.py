# -*- coding: utf-8 -*-
from bobotinho import log

delta = 20


async def routine(bot) -> None:
    connected_channels = [channel.name for channel in bot.connected_channels]
    disconnected_channels = [channel for channel in bot.channels.keys() if channel not in connected_channels]
    for channel in disconnected_channels:
        try:
            await bot.join_channels([channel])
        except Exception:
            bot.channels.pop(channel, None)
    log.info(f"{bot.nick} | #({len(bot.connected_channels)}/{len(bot.channels)}) | {bot._prefix}{len(bot.commands)}")
