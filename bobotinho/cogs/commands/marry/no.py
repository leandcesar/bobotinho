# -*- coding: utf-8 -*-
description = "Recuse o pedido de casamento"


async def func(ctx):
    ctx.response = "não há nenhum pedido de casamento para você"
    for k, v in ctx.bot.cache.get("weddings", {}).items():
        if ctx.author.name == v["name"]:
            ctx.response = f"você recusou o pedido de casamento de @{k} 💔"
            ctx.bot.cache.get("weddings", {}).pop(k, None)
            break
