# -*- coding: utf-8 -*-
import random

aliases = ["%"]
description = "Receba uma probabilidade de 0 a 100"


async def command(ctx):
    percentage = random.randint(0, 1000) / 10
    ctx.response = f"{percentage}%"
