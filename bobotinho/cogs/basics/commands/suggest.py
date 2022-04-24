# -*- coding: utf-8 -*-
from bobotinho.webhook import Webhook

description = "Faça uma sugestão de recurso para o bot"
aliases = ["suggestion"]
usage = "digite o comando e uma sugestão de recurso ou modificação para o bot"


async def command(ctx, *, content: str):
    data = await ctx.bot.api.twitch("avatar", ctx.author.name)
    avatar_url = data["avatar"] if data and data.get("avatar") else None
    if await Webhook().discord(
        ctx.bot.config.suggestions_url,
        content=content,
        user_name=ctx.author.name,
        user_avatar_url=avatar_url,
    ):
        ctx.response = f"sua sugestão foi anotada 💡"
