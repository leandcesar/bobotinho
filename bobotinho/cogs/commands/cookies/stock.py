# -*- coding: utf-8 -*-
from bobotinho.cogs.commands.cookies import resetting_daily
from bobotinho.database import models

description = "Estoque o seu cookie diário caso não queira comê-lo"


async def func(ctx):
    if resetting_daily():
        ctx.response = "a fornada de cookies está sendo preparada, aguarde"
        return
    cookie, _ = await models.Cookie.get_or_create(id=ctx.author.id, name=ctx.author.name)
    if cookie.daily >= 1:
        await cookie.use_daily()
        await cookie.stock()
        ctx.response = "você estocou seu cookie diário"
    else:
        ctx.response = "você já usou seu cookie diário, a próxima fornada sai às 6 da manhã! ⌛"
