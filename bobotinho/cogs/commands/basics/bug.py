# -*- coding: utf-8 -*-
from bobotinho.database import models

description = "Reporte um bug que está ocorrendo no Bot"
usage = "digite o comando e o bug que você encontrou"


async def func(ctx, *, content: str):
    bug = await models.Bug.create(
        name=ctx.author.name,
        channel=ctx.channel.name,
        content=content,
    )
    ctx.response = f"seu bug foi reportado 🐛 (ID {bug.id})"
