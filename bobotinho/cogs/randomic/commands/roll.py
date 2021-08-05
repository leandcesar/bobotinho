# -*- coding: utf-8 -*-
import random

description = "Role um dado e veja o resultado"
usage = "digite o comando e o(s) dado(s) no formato <quantidade>d<lados> (ex: 1d20)"


async def command(ctx, arg: str = ""):
    if not arg or "d" not in arg:
        arg = "1d20"
    dices = arg.lower().split("d")
    amount = int(dices[0].replace(",", ".")) if dices[0] else None
    sides = int(dices[1].replace(",", ".")) if dices[1] else None
    if not amount:
        ctx.response = "especifique a quantidade de dados"
    elif not sides:
        ctx.response = "especifique a quantidade de lados do dado"
    elif amount > 1e4:
        ctx.response = "eu não tenho tantos dados"
    elif amount == 0:
        ctx.response = "eu não consigo rolar sem dados"
    elif amount < 0:
        ctx.response = "não tente tirar meus dados de mim"
    elif sides > 1e4:
        ctx.response = "meus dados não tem tantos lados"
    elif sides == 1:
        ctx.response = f"um dado de {sides} lado? Esse é um exercício topológico interessante..."
    elif sides <= 0:
        ctx.response = f"um dado de {sides} lados? Esse é um exercício topológico interessante..."
    else:
        roll = sum([random.randint(1, round(sides)) for i in range(round(amount))])
        ctx.response = f"você rolou {roll} 🎲"
