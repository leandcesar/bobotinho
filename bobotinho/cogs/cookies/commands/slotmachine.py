# -*- coding: utf-8 -*-
import random

from bobotinho.database.models import Cookie

description = "Aposte seu cookie diário para ter a chance de ganhar outros"
aliases = ["sm"]


async def command(ctx):
    cookie, _ = await Cookie.get_or_create(id=ctx.author.id, name=ctx.author.name)
    if cookie.daily >= 1:
        x, y, z = random.choices("🍇🍊🍋🍒🍉🍐", k=3)
        await cookie.use_daily()
        if x == y == z:
            await cookie.stock(10)
            ctx.response = f"[{x}{y}{z}] você usou seu cookie diário e ganhou 10 cookies! PogChamp"
        elif x == y or x == z or y == z:
            await cookie.stock(3)
            ctx.response = f"[{x}{y}{z}] você usou seu cookie diário e ganhou 3 cookies!"
        else:
            ctx.response = f"[{x}{y}{z}] você perdeu seu cookie diário..."
    else:
        ctx.response = "você já usou seu cookie diário, a próxima fornada sai às 6 da manhã! ⌛"
