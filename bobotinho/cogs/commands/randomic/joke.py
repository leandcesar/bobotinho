# -*- coding: utf-8 -*-
from bobotinho.utils import convert

FILENAME = "bobotinho//data//jokes.txt"
aliases = ["4head", "hahaa"]
description = "Receba uma piada ou trocadilho aleatório"


async def func(ctx):
    joke = convert.txt2randomline(FILENAME)
    ctx.response = f"{joke} 4Head"
