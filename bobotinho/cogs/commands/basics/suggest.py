# -*- coding: utf-8 -*-
from bobotinho.database import models

description = "Faça uma sugestão de recurso para o Bot"
aliases = ["suggestion"]
usage = "digite o comando e uma sugestão de recurso ou modificação para o bot"


async def func(ctx, *, content: str):
    await models.Suggest.create(user_id=ctx.author.name, content=content)
    ctx.response = "sua sugestão foi anotada 📝"
