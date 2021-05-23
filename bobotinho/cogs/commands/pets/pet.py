# -*- coding: utf-8 -*-
from bobotinho.cogs.commands import pets as P
from bobotinho.cogs.commands.pets import petlist, petpat
from bobotinho.database import models
from bobotinho.utils import checks, convert

description = "Veja os pets de um usuário"
aliases = ["pets"]
extra_checks = [checks.is_banword]


async def func(ctx, arg: str = ""):
    name = convert.str2username(arg) or ctx.author.name
    mention = "você" if name == ctx.author.name else f"@{name}"
    if not name:
        ctx.response = "nome de usuário inválido"
    elif arg == "list":
        ctx.response = await petlist.func(ctx)
    elif arg == "pat":
        ctx.response = await petpat.func(ctx)
    elif pets := await models.Pet.filter(user_id=name).all():
        ctx.response = f'{mention} possui {P.join_pets(pets, formatter="{pet} {emoji}")}'
    elif name == ctx.author.name:
        ctx.response = f"adquira um pet em troca de cookies ({ctx.prefix}petlist)"
    else:
        ctx.response = f"{mention} não possui um pet"
