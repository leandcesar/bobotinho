# -*- coding: utf-8 -*-
import random
from bobotinho.database import models

description = "Aposte um cookie para ter x chance de ganhar outros"
aliases = ["sm"]


async def func(ctx):
    cookie, _ = await models.Cookie.get_or_create(user_id=ctx.author.name)
    if cookie.daily:
        x, y, z = random.choices("🍇🍊🍋🍒🍉🍐", k=3)
        await cookie.use_daily()
        if x == y == z:
            await cookie.stock(amount=10)
            ctx.response = f"[{x}{y}{z}] você usou seu cookie diário e ganhou 10 cookies! PogChamp"
        elif x == y or x == z or y == z:
            await cookie.stock(amount=2)
            ctx.response = f"[{x}{y}{z}] você usou seu cookie diário e ganhou 3 cookies!"
        else:
            ctx.response = f"[{x}{y}{z}] você perdeu seu cookie diário..."
    else:
        ctx.response = "você já usou seu cookie diário, a próxima fornada sai às 6 da manhã! ⌛"
