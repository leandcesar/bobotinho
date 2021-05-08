# -*- coding: utf-8 -*-
from bobotinho.database import models

description = "Estoque o seu cookie diário caso não queira comê-lo"


async def func(ctx):
    cookie, _ = await models.Cookie.get_or_create(user_id=ctx.author.name)
    if cookie.daily:
        await cookie.use_daily()
        await cookie.stock()
        ctx.response = "você estocou seu cookie diário"
    else:
        ctx.response = "você já usou seu cookie diário, a próxima fornada sai às 6 da manhã! ⌛"
