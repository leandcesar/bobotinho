# -*- coding: utf-8 -*-
from bobotinho.database import models

description = "Saiba quais são os melhores jogadores da dungeon"


async def func(ctx, arg: str = ""):
    if arg in ["vitoria", "vitorias", "vitória", "vitórias", "win", "wins"]:
        order_by, title = "wins", "vitórias"
    elif arg in ["derrota", "derrotas", "lose", "losses"]:
        order_by, title = "defeats", "derrotas"
    else:
        order_by, title = "level", "dungeons"
    dungeons = await models.Dungeon.filter().order_by("-"+order_by, "-xp").limit(5).all()
    emojis = "🏆🥈🥉🏅🏅"
    tops = " ".join(
        [
            f"{emoji} @{dungeon.user_id} ({getattr(dungeon, order_by)})"
            for emoji, dungeon in zip(emojis, dungeons)
        ]
    )
    ctx.response = f"top {len(dungeons)} {title}: {tops}"
