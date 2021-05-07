# -*- coding: utf-8 -*-
from bobotinho import aiorequests
from bobotinho.database import models

description = "Faça uma sugestão de recurso para o Bot"
aliases = ["suggestion"]
usage = "digite o comando e uma sugestão de recurso ou modificação para o bot"


async def func(ctx, *, content: str):
    suggest = await models.Suggest.create(user_id=ctx.author.name, content=content)
    ctx.response = "sua sugestão foi anotada 📝"
    response = await aiorequests.post(
        ctx.bot.webhook,
        json={
            "resource": "suggestion",
            "id": suggest.id,
            "content": content,
            "author": ctx.author.name,
            "channel": ctx.channel.name,
            "timestamp": ctx.message.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
    )
    if response and response.status == 200:
        await suggest.delete()
