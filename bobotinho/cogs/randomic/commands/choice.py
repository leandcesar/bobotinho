# -*- coding: utf-8 -*-
import random

aliases = ["choose"]
description = 'Dê opções separadas por "ou" e uma delas será escolhida'
usage = 'digite o comando e algumas opções separadas por "ou"'


async def command(ctx, *, content: str):
    if " ou " in content:
        ctx.response = random.choice(content.split(" ou ")).replace("?", "")
