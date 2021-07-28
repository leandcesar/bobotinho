# -*- coding: utf-8 -*-
from bobotinho.database import models

description = "Faça uma sugestão de recurso para o Bot"
aliases = ["suggestion"]
usage = "digite o comando e uma sugestão de recurso ou modificação para o bot"


async def func(ctx, *, content: str):
    suggest = await models.Suggest.create(
        name=ctx.author.name,
        channel=ctx.channel.name,
        content=content,
    )
    ctx.response = f"sua sugestão foi anotada 📝 (ID {suggest.id})"
