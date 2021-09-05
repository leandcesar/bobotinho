# -*- coding: utf-8 -*-
from bobotinho.apis import Twitch
from bobotinho.utils import convert

description = "Receba o link da foto de perfil de algum usuário"
aliases = ["icon"]
usage = "digite o comando e o nome de alguém para receber o link da foto de perfil"


async def command(ctx, arg: str = ""):
    name = convert.str2name(arg, default=ctx.author.name)
    avatar = await Twitch.avatar(name)
    if not avatar:
        ctx.response = "não foi possível verificar isso"
    elif "não existe" in avatar:
        ctx.response = avatar
    elif name == ctx.author.name:
        ctx.response = f"sua foto de perfil: {avatar}"
    else:
        ctx.response = f"foto de perfil de @{name}: {avatar}"
