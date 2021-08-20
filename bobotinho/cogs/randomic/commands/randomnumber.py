# -*- coding: utf-8 -*-
import random

description = "Gere um número aleatório dentre o intervalo fornecido"
usage = "digite o comando e o número inicial e final do intervalo separados por espaço"
aliases = ["rng"]


async def command(ctx, arg1: str = "1", arg2: str = "100"):
    if arg1.isdigit() and arg2.isdigit():
        init = int(arg1)
        end = int(arg2)
        if init > end:
            init, end = end, init
        if init == end:
            ctx.response = "não será aleatório com esse intervalo..."
        else:
            number = random.randint(init, end)
            ctx.response = f"aqui está um número aléatorio: {number}"
