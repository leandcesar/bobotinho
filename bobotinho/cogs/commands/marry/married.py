# -*- coding: utf-8 -*-
from bobotinho.database import models
from bobotinho.utils import checks, convert, timetools

description = "Saiba quando algum usuário se casou"
extra_checks = [checks.banword]


async def func(ctx, arg: str = ""):
    name = convert.str2username(arg) or ctx.author.name
    mention = "você" if name == ctx.author.name else f"@{name}"
    if not name:
        ctx.response = "nome de usuário inválido"
    elif name == ctx.bot.nick:
        ctx.response = "nunca me casarei com ninguém"
    elif not (user := await models.User.get_or_none(name=name)):
        ctx.response = f"@{name} ainda não foi registrado (não usou nenhum comando)"
    elif arg and not user.mention:
        ctx.response = "esse usuário optou por não permitir mencioná-lo"
    elif wedding := await models.Wedding.get_or_none(user_1_id=user.id, divorced=False):
        date = timetools.format(wedding.created_at)
        user_2 = await models.User.get_or_none(id=wedding.user_2_id)
        ctx.response = f"{mention} se casou com @{user_2.name} em {date}"
    elif wedding := await models.Wedding.get_or_none(user_2_id=user.id, divorced=False):
        date = timetools.format(wedding.created_at)
        user_1 = await models.User.get_or_none(id=wedding.user_1_id)
        ctx.response = f"{mention} se casou com @{user_1.name} em {date}"
    else:
        ctx.response = f"{mention} não está casado com ninguém"
