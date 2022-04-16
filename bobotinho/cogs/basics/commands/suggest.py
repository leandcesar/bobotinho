# -*- coding: utf-8 -*-
from bobotinho.webhook import Webhook

description = "Faça uma sugestão de recurso para o bot"
aliases = ["suggestion"]
usage = "digite o comando e uma sugestão de recurso ou modificação para o bot"


async def command(ctx, *, content: str):
    payload = {
        "title": "Sugestão",
        "description": content,
        "color": ctx.bot.config.color,
        "author_name": ctx.author.name,
        "footer_text": ctx.channel.name,
    }
    await Webhook.discord(ctx.bot.config.bugs_url, payload=payload)
    ctx.response = f"sua sugestão foi anotada 💡"
