# -*- coding: utf-8 -*-
from bobotinho.utils import convert

FILENAME = "bobotinho//data//magicball.txt"
aliases = ["8ball"]
description = "Tenha sua pergunta respondida por uma previsão"
usage = "digite o comando e uma pergunta para receber uma previsão"


async def command(ctx, *, content: str):
    predict = convert.txt2randomline(FILENAME)
    ctx.response = f"{predict} 🎱"
