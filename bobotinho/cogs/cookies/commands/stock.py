# -*- coding: utf-8 -*-
from bobotinho.database.models import Cookie

description = "Estoque o seu cookie diário, caso não queira usá-lo"


async def command(ctx):
    cookie, _ = await Cookie.get_or_create(id=ctx.author.id, name=ctx.author.name)
    if cookie.daily >= 1:
        await cookie.use_daily()
        await cookie.stock()
        ctx.response = "você estocou seu cookie diário"
    else:
        ctx.response = "você já usou seu cookie diário, a próxima fornada sai às 6 da manhã! ⌛"
