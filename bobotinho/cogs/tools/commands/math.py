# -*- coding: utf-8 -*-
from bobotinho.apis import Math

description = "Saiba o resultado de alguma expressão matemática"
usage = "digite o comando e uma expressão matemática (ex: 1+1)"


async def command(ctx, *, content: str):
    response = await Math.calculate(content)
    if response:
        result = response.replace("Infinity", "infinito").replace("NaN", "🤯")
        ctx.response = result
