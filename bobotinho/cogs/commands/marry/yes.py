# -*- coding: utf-8 -*-
from bobotinho.database import models

description = "Aceite o pedido de casamento"


async def func(ctx):
    if wedding := ctx.bot.cache.get("weddings", {}).pop(ctx.author.name, None):
        cookie = await models.Cookie.get(name=wedding["name"])
        if cookie.stocked < 100:
            ctx.response = (
                f"parece que @{cookie.user_id} gastou todos os cookies "
                "que eram pra aliança... o casamento precisou ser cancelado"
            )
        else:
            await models.Wedding.create(user_1_id=cookie.user_id, user_2_id=ctx.author.name)
            cookie.stocked -= 100
            await cookie.save()
            ctx.response = f'você aceitou se casar com @{cookie.user_id}, felicidades! 🎉💞'
    else:
        ctx.response = "não há nenhum pedido de casamento para você"
