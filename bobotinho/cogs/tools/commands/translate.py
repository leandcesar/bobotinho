# -*- coding: utf-8 -*-
import re

description = "Saiba a tradução de alguma mensagem"
usage = "digite o comando e um texto para ser traduzido"


async def command(ctx, arg: str, *, content: str = ""):
    if match := re.match(r"(\w{2})?->(\w{2})?", arg):  # source->target or source-> or ->target
        source, target = match.groups()
    else:
        content = f"{arg} {content}"
        source = target = None

    translation = await ctx.bot.api.translate(content, source if source else "auto", target if target else "pt")
    if translation and translation != content:
        ctx.response = translation
    else:
        ctx.response = "não foi possível traduzir isso"
