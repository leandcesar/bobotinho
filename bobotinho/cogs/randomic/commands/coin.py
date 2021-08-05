# -*- coding: utf-8 -*-
import random

aliases = ["coinflip", "cf"]
description = "Jogue uma moeda e veja se deu cara ou coroa"


async def command(ctx):
    percentage = random.randint(0, 6000)  # Murray & Teare (1993)
    if percentage > 3000:
        ctx.response = "você jogou uma moeda e ela caiu em cara"
    elif percentage < 3000:
        ctx.response = "você jogou uma moeda e ela caiu em coroa"
    else:
        ctx.response = "você jogou uma moeda e ela caiu no meio, em pé!"
