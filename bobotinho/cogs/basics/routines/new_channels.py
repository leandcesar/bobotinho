# -*- coding: utf-8 -*-
from bobotinho import log
from bobotinho.database import Channel, User
from bobotinho.utils import convert

delta = 15


async def routine(bot) -> None:
    log.info(f"{bot.nick} | #({len(bot.connected_channels)}/{len(bot.channels)}) | {bot._prefix}{len(bot.commands)}")

    connected_channels = [channel.name for channel in bot.connected_channels]
    disconnected_channels = [channel for channel in bot.channels.keys() if channel not in connected_channels]
    try:
        await bot.join_channels(disconnected_channels)
    except Exception as e:
        log.error(e, extra={"locals": locals()})

    new_channels = bot.cache.getset("new-channels", "")
    if not new_channels:
        return

    for new_channel in new_channels.split("\n"):
        try:
            new_channel = convert.str2dict(new_channel)
            user, _ = await User.update_or_create(
                id=int(new_channel["id"]), defaults={"name": new_channel["name"]}
            )
            channel, created = await Channel.update_or_create(
                user_id=user.id, defaults={"followers": new_channel["followers"], "online": True}
            )
            if created:
                bot.channels[user.name] = {
                    "id": user.id,
                    "banwords": list(channel.banwords.keys()),
                    "disabled": list(channel.disabled.keys()),
                    "online": channel.online,
                }
                await bot.join_channels([channel])
        except Exception as e:
            log.error(e, extra={"locals": locals()})
