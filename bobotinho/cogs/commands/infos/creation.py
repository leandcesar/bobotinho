# -*- coding: utf-8 -*-
from bobotinho.apis.twitch import TwitchAPI
from bobotinho.utils import checks, convert

description = "Saiba quando algum usuário criou sua conta"
aliases = ["create"]
usage = "digite o comando e o nome de alguém para saber a data de criação da conta"
extra_checks = [checks.banword]


async def func(ctx, arg: str = ""):
    name = convert.str2name(arg, default=ctx.author.name)
    if name == ctx.bot.nick:
        ctx.response = "eu sempre existi..."
    else:
        creation = await TwitchAPI.creation(name)
        mention = "você" if name == ctx.author.name else f"@{name}"
        if not creation:
            ctx.response = "não foi possível verificar isso"
        elif "não existe" in creation:
            ctx.response = creation
        else:
            ctx.response = f"{mention} criou a conta em {creation}"
