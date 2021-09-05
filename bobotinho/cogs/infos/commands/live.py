# -*- coding: utf-8 -*-
from bobotinho.apis import Twitch
from bobotinho.utils import convert

description = "Veja as informações da live de algum canal"
usage = "digite o comando e o nome de um canal para saber as informações da live"
aliases = ["stream"]


async def command(ctx, arg: str = ""):
    name = convert.str2name(arg, default=ctx.channel.name)
    uptime = await Twitch.uptime(name)
    mention = "você" if name == ctx.author.name else f"@{name}"
    if not uptime:
        ctx.response = "não foi possível verificar isso"
    elif "não existe" in uptime:
        ctx.response = uptime
    elif (title := await Twitch.title(name)) and "is offline" in uptime:
        ctx.response = f"{mention} está offline: {title}"
    elif "is offline" in uptime:
        ctx.response = f"{mention} está offline"
    elif (game := await Twitch.game(name)) and title:
        ctx.response = f"{mention} está streamando {game}: {title} ({uptime})"
    elif title:
        ctx.response = f"{mention} está online: {title} ({uptime})"
    elif game:
        ctx.response = f"{mention} está streamando {game} ({uptime})"
    else:
        ctx.response = f"{mention} está online ({uptime})"
