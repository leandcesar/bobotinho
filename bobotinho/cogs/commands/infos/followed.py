# -*- coding: utf-8 -*-
from bobotinho.apis.twitch import TwitchAPI
from bobotinho.utils import checks, convert

description = "Saiba quando algum usuário segue algum canal"
extra_checks = [checks.banword]


async def func(ctx, arg1: str = "", arg2: str = ""):
    name = convert.str2name(arg1, default=ctx.author.name)
    channel = convert.str2name(arg2, default=ctx.channel.name)
    if name and channel:
        followed = await TwitchAPI.followed(channel, name)
        name = "você" if name == ctx.author.name else f"@{name}"
        channel = "você" if channel == ctx.author.name else f"@{channel}"
    if name == f"@{ctx.bot.nick}":
        ctx.response = f"eu sempre estive em {channel}..."
    elif name == channel:
        ctx.response = f"{name} não pode se seguir"
    elif not followed:
        ctx.response = f"{name} não segue {channel}"
    elif "não existe" in followed:
        ctx.response = followed
    else:
        ctx.response = f"{name} seguiu {channel} em {followed}"
