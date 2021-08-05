# -*- coding: utf-8 -*-
from bobotinho.apis import Twitch
from bobotinho.utils import convert

description = "Saiba quando algum usuário criou sua conta"
aliases = ["create"]
usage = "digite o comando e o nome de alguém para saber a data de criação da conta"


async def command(ctx, arg: str = ""):
    name = convert.str2name(arg, default=ctx.author.name)
    if name == ctx.bot.nick:
        ctx.response = "eu sempre existi..."
    else:
        creation = await Twitch.creation(name)
        mention = "você" if name == ctx.author.name else f"@{name}"
        if not creation:
            ctx.response = "não foi possível verificar isso"
        elif "não existe" in creation:
            ctx.response = creation
        else:
            ctx.response = f"{mention} criou a conta em {creation}"
