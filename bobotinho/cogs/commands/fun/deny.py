# -*- coding: utf-8 -*-
description = "Recuse o desafio para lutar"


async def func(ctx):
    if fight := ctx.bot.cache.get("fights", {}).pop(ctx.author.name, None):
        ctx.response = f'você recusou o desafio contra @{fight["name"]} LUL'
    else:
        ctx.response = "você não tem desafios para recusar"
