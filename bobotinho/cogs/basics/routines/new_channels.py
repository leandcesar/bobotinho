# -*- coding: utf-8 -*-
from bobotinho.database.models import Channel
from bobotinho import log

delta = 30


async def routine(bot) -> None:
    channels_id = [channel["id"] for channel in bot.channels.values()]
    channels = await Channel.filter(user_id__not_in=channels_id).all()
    for channel in channels:
        await channel.fetch_related("user")
        if channel.user.name in bot.channels:
            log.warning(f"Channel already added: <{channel}>")
            continue
        try:
            await bot.join_channels([channel.user.name])
            bot.channels[channel.user.name] = {
                "id": channel.user_id,
                "banwords": list(channel.banwords.keys()),
                "disabled": list(channel.disabled.keys()),
                "online": channel.online,
            }
            response = (
                f"@{channel.user.name}, obrigado por me adicionar, "
                f'veja meus comandos com "{bot._prefix}help"'
            )
            await bot.get_channel(channel.user.name).send(response)
            log.info(f"#{channel.user.name} @{bot.nick}: {response}")
        except Exception as e:
            log.exception(e, extra={"locals": locals()})
