# -*- coding: utf-8 -*-
import re

from bobotinho.apis import Translator
from bobotinho import log

description = "Saiba a tradução de alguma mensagem"
usage = "digite o comando e um texto para ser traduzido"


async def command(ctx, arg: str, *, content: str = ""):
    if match := re.match(r"(\w{2})?->(\w{2})?", arg):  # source->target or source-> or ->target
        source, target = match.groups()
    else:
        content = f"{arg} {content}"
        source = target = None
    try:
        ctx.response = Translator.translate(
            text=content,
            source=source if source else "auto",
            target=target if target else "pt",
        )
    except Exception as e:
        log.exception(e)
        ctx.response = "não foi possível traduzir isso"
