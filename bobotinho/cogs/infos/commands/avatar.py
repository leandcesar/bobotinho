# -*- coding: utf-8 -*-
from bobotinho.utils import convert

description = "Receba o link da foto de perfil de algum usuário"
aliases = ["icon"]
usage = "digite o comando e o nome de alguém para receber o link da foto de perfil"


async def command(ctx, arg: str = ""):
    name = convert.str2name(arg, default=ctx.author.name)
    data = await ctx.bot.api.twitch("avatar", name)
    if data and data["avatar"]:
        avatar = data["avatar"]
        if name == ctx.author.name:
            ctx.response = f"sua foto de perfil: {avatar}"
        elif name == ctx.bot.nick:
            ctx.response = f"minha foto de perfil: {avatar}"
        else:
            ctx.response = f"foto de perfil de @{name}: {avatar}"
    else:
        ctx.response = f"{mention} não existe"
