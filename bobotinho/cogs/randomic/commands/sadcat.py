# -*- coding: utf-8 -*-
from bobotinho.utils import convert

FILENAME = "bobotinho//data//sadcats.txt"
aliases = ["sc"]
description = "Receba a foto de um gatinho triste aleatório"


async def command(ctx):
    id_imgur = convert.txt2randomline(FILENAME)
    ctx.response = f"https://i.imgur.com/{id_imgur} 😿"
