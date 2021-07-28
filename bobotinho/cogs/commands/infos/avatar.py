# -*- coding: utf-8 -*-
from bobotinho.apis.twitch import TwitchAPI
from bobotinho.utils import checks, convert

description = "Receba o link da foto de perfil de algum usuário"
usage = "digite o comando e o nome de alguém para receber o link da foto de perfil"
extra_checks = [checks.banword]


async def func(ctx, arg: str = ""):
    name = convert.str2name(arg, default=ctx.author.name)
    avatar = await TwitchAPI.avatar(name)
    if not avatar:
        ctx.response = "não foi possível verificar isso"
    elif "não existe" in avatar:
        ctx.response = avatar
    elif name == ctx.author.name:
        ctx.response = f"sua foto de perfil: {avatar}"
    else:
        ctx.response = f"foto de perfil de @{name}: {avatar}"
