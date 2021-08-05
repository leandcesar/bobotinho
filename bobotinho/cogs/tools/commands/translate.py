# -*- coding: utf-8 -*-
import re

from bobotinho.apis import Translator
from bobotinho import log

description = "Saiba a tradução de alguma mensagem"
usage = "digite o comando e um texto para ser traduzido"


async def command(ctx, arg: str, *, content: str = ""):
    src = dest = None
    if match := re.match(r"(\w{2})?->(\w{2})?", arg):  # scr->dest or scr-> or ->dest
        src, dest = match.groups()
    else:
        content = f"{arg} {content}"
    src = src if src else "auto"
    dest = dest if dest else "en" if Translator.detect(content) == "pt" else "pt"
    try:
        translation = Translator.translate(content, dest, src)
    except Exception as e:
        log.exception(e)
        translation = None
    if translation and translation != content:
        ctx.response = f"{src}->{dest}: {translation}"
    else:
        ctx.response = "não foi possível traduzir isso"
