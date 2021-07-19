# -*- coding: utf-8 -*-
from bobotinho.utils import checks, convert

description = "Faça carinho em alguém do chat"
usage = "digite o comando e o nome de alguém para fazer carinho"
extra_checks = [checks.banword]


async def func(ctx, arg: str):
    name = convert.str2name(arg)
    if name == ctx.bot.nick:
        ctx.response = "😊"
    elif name == ctx.author.name:
        ctx.response = "você tentou fazer cafuné em si memso... FeelsBadMan"
    else:
        ctx.response = f"você fez cafuné em @{name} 😊"
