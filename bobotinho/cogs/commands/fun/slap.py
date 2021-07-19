# -*- coding: utf-8 -*-
from bobotinho.utils import checks, convert

description = "Dê um tapa em alguém do chat"
usage = "digite o comando e o nome de alguém que mereça levar uns tapas"
extra_checks = [checks.banword]


async def func(ctx, arg: str):
    name = convert.str2name(arg)
    if name == ctx.bot.nick:
        ctx.response = "vai bater na mãe 😠"
    elif name == ctx.author.name:
        ctx.response = "você se deu um tapa... 😕"
    else:
        ctx.response = f"você deu um tapa em @{name} 👋"
