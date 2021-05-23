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
    elif wedding := await models.Wedding.get_or_none(user_1_id=name, divorced=False):
        timeago = timetools.timeago(wedding.created_at)
        ctx.response = f"{mention} está casado com @{wedding.user_2_id} há {timeago}"
    elif wedding := await models.Wedding.get_or_none(user_2_id=name, divorced=False):
        timeago = timetools.timeago(wedding.created_at)
        ctx.response = f"{mention} está casado com @{wedding.user_1_id} há {timeago}"
    else:
        ctx.response = f"{mention} não está casado com ninguém"