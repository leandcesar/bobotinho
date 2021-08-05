# -*- coding: utf-8 -*-
from bobotinho.database.models import Cookie
from bobotinho.utils import convert

description = "Veja quantos cookies algum usuário já comeu"
aliases = ["cc"]


async def command(ctx, arg: str = ""):
    name = convert.str2name(arg, default=ctx.author.name)
    mention = "você" if name == ctx.author.name else f"@{name}"
    if name == ctx.bot.nick:
        ctx.response = "eu tenho cookies infinitos, e distribuo uma fração deles para vocês"
    elif cookie := await Cookie.get_or_none(name=name):
        ctx.response = (
            f"{mention} já comeu {cookie.count} cookies, presenteou {cookie.donated}, "
            f"foi presenteado com {cookie.received} e tem {cookie.stocked} estocados"
        )
    else:
        ctx.response = f"{mention} ainda não comeu nenhum cookie"
