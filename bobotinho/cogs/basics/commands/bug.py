# -*- coding: utf-8 -*-
from bobotinho.webhook import Webhook

description = "Reporte um bug que está ocorrendo no Bot"
usage = "digite o comando e o bug que você encontrou"


async def command(ctx, *, content: str):
    data = await ctx.bot.api.twitch("avatar", ctx.author.name)
    avatar_url = data["avatar"] if data and data.get("avatar") else None
    if await Webhook().discord(
        ctx.bot.config.bugs_url,
        content=content,
        user_name=ctx.author.name,
        user_avatar_url=avatar_url,
    ):
        ctx.response = f"seu bug foi reportado 🐛"
