# -*- coding: utf-8 -*-
from bobotinho.database import models
from bobotinho.utils import checks, convert, timetools

description = "Saiba a última vez que alguém foi visto"
aliases = ["ls"]
usage = "digite o comando e o nome de alguém para saber quando foi visto pela última vez"
extra_checks = [checks.is_banword]


async def func(ctx, arg: str):
    name = convert.str2username(arg)
    if not name:
        ctx.response = "nome de usuário inválido"
    elif name == ctx.bot.nick:
        ctx.response = "eu estou em todos os lugares, a todo momento..."
    elif name == ctx.author.name:
        ctx.response = "você foi visto pela última vez aqui ☝️"
    elif await models.User.exists(name=name):
        user = await models.User.get(name=name)
        timeago = timetools.date_in_full(user.updated_ago)
        ctx.response = (
            f"@{name} foi visto em @{user.channel} "
            f"pela última vez: {user.content} ({timeago})"
        )
    else:
        ctx.response = f"@{name} ainda não foi registrado (não usou nenhum comando)"
