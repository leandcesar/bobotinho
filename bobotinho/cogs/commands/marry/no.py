# -*- coding: utf-8 -*-
description = "Recuse o pedido de casamento"


async def func(ctx):
    if wedding := ctx.bot.cache.get("weddings", {}).pop(ctx.author.name, None):
        name = wedding["name"]
        ctx.response = f"você recusou o pedido de casamento de @{name} 💔"
    else:
        ctx.response = "não há nenhum pedido de casamento para você"
