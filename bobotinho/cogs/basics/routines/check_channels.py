# -*- coding: utf-8 -*-
from bobotinho import log
from bobotinho.utils import convert

delta = 10


async def routine(bot) -> None:
    try:
        connected_channels = [channel.name for channel in bot.connected_channels]
        disconnected_channels = [channel for channel in bot.channels.keys() if channel not in connected_channels]
        await bot.join_channels(disconnected_channels)
    except Exception as e:
        log.exception(e, extra={"locals": locals()})
    finally:
        unjoined_channels = bot.cache.get("unjoined-channels")
        unjoined_channels = convert.str2dict(unjoined_channels)
        unjoined_channels = {
            channel: unjoined_channels.get(channel, 0) + 1
            for channel in disconnected_channels
        }
        for channel in unjoined_channels:
            if unjoined_channels[channel] > 3:
                bot.channels.pop(channel)
                log.warning(f"The channel '{channel}' was unable to be joined and has been removed.")
        unjoined_channels = convert.dict2str(unjoined_channels)
        bot.cache.set("unjoined-channels", unjoined_channels)
