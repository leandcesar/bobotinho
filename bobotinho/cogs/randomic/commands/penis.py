# -*- coding: utf-8 -*-
description = "É... é isso mesmo"


async def command(ctx):
    length = int(ctx.author.id) % 30
    if length <= 6:
        length = 6
    if length <= 10:
        ctx.response = f"{length}cm 🤏"
    elif length <= 15:
        ctx.response = f"{length}cm 🪱"
    elif length <= 20:
        ctx.response = f"{length}cm 🍌"
    else:
        ctx.response = f"{length}cm 🍆"
