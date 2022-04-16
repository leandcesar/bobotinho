# -*- coding: utf-8 -*-
from bobotinho.webhook import Webhook

description = "Reporte um bug que está ocorrendo no Bot"
usage = "digite o comando e o bug que você encontrou"


async def command(ctx, *, content: str):
    payload = {
        "title": "Bug",
        "description": content,
        "color": ctx.bot.config.color,
        "author_name": ctx.author.name,
        "footer_text": ctx.channel.name,
    }
    await Webhook.discord(ctx.bot.config.bugs_url, payload=payload)
    ctx.response = f"seu bug foi reportado 🐛"
