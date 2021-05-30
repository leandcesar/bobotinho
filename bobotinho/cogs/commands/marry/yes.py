# -*- coding: utf-8 -*-
from bobotinho.database import models

description = "Aceite o pedido de casamento"


async def func(ctx):
    if wedding := ctx.bot.cache.get("weddings", {}).pop(ctx.author.name, None):
        cookie = await models.Cookie.get(name=wedding["name"])
        if cookie.stocked < 100:
            ctx.response = (
                f'parece que @{wedding["name"]} gastou todos os cookies '
                "que eram pra aliança... o casamento precisou ser cancelado"
            )
        else:
            if not await models.Cookie.exists(id=ctx.author.id):
                await models.Cookie.create(id=ctx.author.id)
            await models.Wedding.create(user_1_id=cookie.id, user_2_id=ctx.author.id)
            cookie.stocked -= 100
            await cookie.save()
            ctx.response = f'você aceitou se casar com @{wedding["name"]}, felicidades! 🎉💞'
    else:
        ctx.response = "não há nenhum pedido de casamento para você"
