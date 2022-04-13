# -*- coding: utf-8 -*-
from bobotinho import log
from bobotinho.database import Channel, User
from bobotinho.utils import convert

delta = 10


async def routine(bot) -> None:
    new_channels = bot.cache.getset("new-channels", "")
    if not new_channels:
        return
    for new_channel in new_channels.split("\n"):
        try:
            new_channel = convert.str2dict(new_channel)
            user, _ = await User.update_or_create(
                id=int(new_channel["id"]), defaults={"name": new_channel["name"]}
            )
            channel, _ = await Channel.update_or_create(
                user_id=user.id, defaults={"followers": new_channel["followers"]}
            )
            bot.add_channel(
                user.name,
                user.id,
                list(channel.banwords.keys()),
                list(channel.disabled.keys()),
                channel.online,
            )
        except Exception as e:
            log.exception(e, extra={"locals": locals()})
