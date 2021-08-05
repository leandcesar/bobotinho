# -*- coding: utf-8 -*-
description = "Recuse o pedido de casamento"


async def command(ctx):
    if name := ctx.bot.cache.get(f"marry-{ctx.author.name}"):
        ctx.response = f"você recusou o pedido de casamento de @{name} 💔"
        ctx.bot.cache.delete(f"marry-{ctx.author.name}")
    else:
        ctx.response = "não há nenhum pedido de casamento para você"
