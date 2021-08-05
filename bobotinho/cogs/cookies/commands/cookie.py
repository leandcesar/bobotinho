# -*- coding: utf-8 -*-
from bobotinho.cogs.cookies import resetting_daily
from bobotinho.database.models import Cookie
from bobotinho.utils import convert

FILENAME = "bobotinho//data//cookies.txt"
description = "Coma um biscoito da sorte e receba uma frase"


async def command(ctx, arg: str = ""):
    if resetting_daily():
        ctx.response = "a fornada de cookies está sendo preparada, aguarde"
        return
    amount = convert.str2int(arg) or 1
    cookie, _ = await Cookie.get_or_create(id=ctx.author.id, name=ctx.author.name)
    if amount == 0:
        ctx.response = "você não comeu nada, uau!"
    elif amount < 0:
        ctx.response = f"para comer {amount} cookies, você deve primeiro reverter a entropia"
    elif cookie.stocked + cookie.daily >= amount:
        await cookie.consume(amount)
        if amount > 1:
            ctx.response = f"você comeu {amount} cookies de uma só vez 🥠"
        else:
            quote = convert.txt2randomline(FILENAME)
            ctx.response = f"{quote} 🥠"
    elif amount > 1:
        ctx.response = f"você não tem {amount} cookies estocados para comer"
    else:
        ctx.response = "você já usou seu cookie diário, a próxima fornada sai às 6 da manhã! ⌛"
