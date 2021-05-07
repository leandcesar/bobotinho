# -*- coding: utf-8 -*-
description = "Cancele o desafio para lutar"


async def func(ctx):
    ctx.response = "você não tem desafios para cancelar"
    for k, v in ctx.bot.cache.get("fights", {}).items():
        if ctx.author.name == v["name"]:
            ctx.response = f"você cancelou o desafio contra @{k}"
            ctx.bot.cache.get("fights", {}).pop(k, None)
            break
