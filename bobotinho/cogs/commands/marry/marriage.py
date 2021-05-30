# -*- coding: utf-8 -*-
from bobotinho.database import models
from bobotinho.utils import checks, convert, timetools

description = "Saiba há quanto tempo algum usuário está casado"
aliases = ["ma"]
extra_checks = [checks.is_banword]


async def func(ctx, arg: str = ""):
    name = convert.str2username(arg) or ctx.author.name
    mention = "você" if name == ctx.author.name else f"@{name}"
    if not name:
        ctx.response = "nome de usuário inválido"
    elif name == ctx.bot.nick:
        ctx.response = "nunca me casarei com ninguém"
    elif not (user := await models.User.get_or_none(name=name)):
        ctx.response = f"@{name} ainda não foi registrado (não usou nenhum comando)"
    elif wedding := await models.Wedding.get_or_none(user_1_id=user.id, divorced=False):
        timeago = timetools.timeago(wedding.created_at)
        user_2 = await models.User.get_or_none(id=wedding.user_2_id)
        ctx.response = f"{mention} está casado com @{user_2.name} há {timeago}"
    elif wedding := await models.Wedding.get_or_none(user_2_id=user.id, divorced=False):
        timeago = timetools.timeago(wedding.created_at)
        user_1 = await models.User.get_or_none(id=wedding.user_1_id)
        ctx.response = f"{mention} está casado com @{user_1.name} há {timeago}"
    else:
        ctx.response = f"{mention} não está casado com ninguém"
