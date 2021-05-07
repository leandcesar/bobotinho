# -*- coding: utf-8 -*-
import re

from bobotinho.apis import translate
from bobotinho.logger import log

description = "Saiba a tradução de alguma mensagem"
aliases = ["tl"]
usage = "digite o comando e um texto para ser traduzido"


async def func(ctx, arg: str, *, content: str = ""):
    src = dest = None
    if match := re.match(r"(\w{2})?->(\w{2})?", arg):  # scr->dest or scr-> or ->dest
        src, dest = match.groups()
    else:
        content = f"{arg} {content}"
    src = src if src else "auto"
    dest = dest if dest else "en" if translate.TranslateApi.detect(content)[0] == "pt" else "pt"
    try:
        translation = translate.TranslateApi.translate(content, dest, src)
    except Exception as e:
        log.exception(e)
        translation = None
    if translation and translation != content:
        # TODO: se a tradução for uma banword... vish
        ctx.response = f"{src}->{dest}: {translation}"
    else:
        ctx.response = "não foi possível traduzir isso"
