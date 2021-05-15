# -*- coding: utf-8 -*-
from bobotinho.database import models
from bobotinho.utils import checks, convert

description = "Veja quantos cookies algum usuário já comeu"
aliases = ["cc"]
extra_checks = [checks.is_banword]


async def func(ctx, arg: str = ""):
    name = convert.str2username(arg) or ctx.author.name
    mention = "você" if name == ctx.author.name else f"@{name}"
    if not name:
        ctx.response = "nome de usuário inválido"
    elif name == ctx.bot.nick:
        ctx.response = "eu tenho cookies infinitos, e distribuo uma fração deles para vocês"
    elif cookie := await models.Cookie.get_or_none(name=name):
        ctx.response = (
            f"{mention} já comeu {cookie.count} cookies, presenteou {cookie.donated}, "
            f"foi presenteado com {cookie.received} e tem {cookie.stocked} estocados"
        )
    else:
        ctx.response = f"{mention} ainda não comeu nenhum cookie"
