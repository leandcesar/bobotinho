# -*- coding: utf-8 -*-
import random

description = "Sorteia uma palavra da mensagem informada"
usage = "digite o comando e opções separadas por espaço"


async def command(ctx, *, content: str):
    delimiter = "," if "," in content else " "
    options = content.split(delimiter)
    ctx.response = random.choice(options)
