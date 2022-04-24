# -*- coding: utf-8 -*-
from bobotinho.utils import convert

description = "Veja as informações da live de algum canal"
usage = "digite o comando e o nome de um canal para saber as informações da live"
aliases = ["stream"]


async def command(ctx, arg: str = ""):
    name = convert.str2name(arg, default=ctx.channel.name)
    data = await ctx.bot.api.twitch("game,title,total_views,uptime,viewers", name)
    mention = "você" if name == ctx.author.name else f"@{name}"
    if data and (data["title"] or data["uptime"]):
        game = data["game"]
        title = data["title"]
        uptime = data["uptime"]
        if not uptime or "offline" in uptime:
            ctx.response = f"{mention} está offline"
        elif game:
            ctx.response = f"{mention} está streamando {game}"
        else:
            ctx.response = f"{mention} está online"
        if title:
            ctx.response += f": {title}"
        if uptime and "offline" not in uptime:
            ctx.response += f" ({uptime})"
    else:
        ctx.response = f"{mention} não existe"
