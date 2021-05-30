# -*- coding: utf-8 -*-
from bobotinho.database import models

description = "Veja quais são os maiores comedores ou doadores de cookies"


async def func(ctx, arg: str = ""):
    if arg in ["gift", "gifts", "give", "gives", "giver", "givers"]:
        order_by, title = "donated", "givers"
    else:
        order_by, title = "count", "cookiers"
    cookies = await models.Cookie.filter().order_by("-"+order_by).limit(5).all()
    users = [await models.User.get(id=cookie.id) for cookie in cookies]
    emojis = "🏆🥈🥉🏅🏅"
    tops = " ".join(
        [
            f"{emoji} @{user.name} ({getattr(cookie, order_by)})"
            for emoji, user, cookie in zip(emojis, users, cookies)
        ]
    )
    ctx.response = f"top {len(cookies)} {title}: {tops}"
