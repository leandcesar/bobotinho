# -*- coding: utf-8 -*-
from bobotinho.apis import math

description = "Saiba o resultado de alguma expressão matemática"
usage = "digite o comando e uma expressão matemática (ex: 1+1)"


async def func(ctx, *, content: str):
    response = await math.MathAPI.calculate(content)
    if response:
        result = response.replace("Infinity", "infinito").replace("NaN", "🤯")
        ctx.response = result
