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
    players = await models.Player.filter().order_by("-"+order_by, "-xp").limit(5).all()
    emojis = "🏆🥈🥉🏅🏅"
    tops = " ".join(
        [
            f"{emoji} @{player.name} ({getattr(player, order_by)})"
            for emoji, player in zip(emojis, players)
        ]
    )
    ctx.response = f"top {len(players)} {title}: {tops}"
