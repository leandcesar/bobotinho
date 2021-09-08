# -*- coding: utf-8 -*-
from bobotinho.database.models import Suggest

description = "Faça uma sugestão de recurso para o bot"
aliases = ["suggestion"]
usage = "digite o comando e uma sugestão de recurso ou modificação para o bot"


async def command(ctx, *, content: str):
    suggest = await Suggest.create(
        author=ctx.author.name,
        source=ctx.channel.name,
        content=content,
    )
    ctx.response = f"sua sugestão foi anotada 📝 (ID {suggest.id})"
