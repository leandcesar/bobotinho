# -*- coding: utf-8 -*-
import random

description = "Gere uma cor hexadecimal aleatória"
aliases = ["rcg"]


async def command(ctx):
    hex = random.randint(0, 0xFFFFFF)
    color = f"#{hex:06X}"
    ctx.response = f"aqui está uma cor aleatória: {color}"
