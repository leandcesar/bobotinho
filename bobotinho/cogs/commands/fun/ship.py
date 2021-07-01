# -*- coding: utf-8 -*-
from bobotinho.utils import checks, convert

description = "Faça um ship entre o nome de duas pessoas"
usage = "digite o comando e o nome de duas pessoas para shipá-los"
extra_checks = [checks.banword]


async def func(ctx, arg1: str, arg2: str = ""):
    name1 = convert.str2username(arg1)
    name2 = convert.str2username(arg2)
    if name1 and not name2:
        name1, name2 = ctx.author.name, name1
    if not name1:
        ctx.response = "nome de usuário inválido"
    elif name1 == name2:
        ctx.response = "uma pessoa não pode ser shipada com ela mesma..."
    else:
        ship1 = name1[:len(name1)//2 + 1] if len(name1) > 2 else name1
        ship2 = name2[len(name2)//2:] if len(name2) > 2 else name2
        ctx.response = f"{name1} & {name2}: {ship1 + ship2} 😍"
