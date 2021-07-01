# -*- coding: utf-8 -*-
import random

from bobotinho.utils import checks

aliases = ["choose"]
description = 'Dê opções separadas por "ou" e uma delas será escolhida'
usage = 'digite o comando e algumas opções separadas por "ou"'
extra_checks = [checks.banword]


async def func(ctx, *, content: str):
    if " ou " in content:
        ctx.response = random.choice(content.split(" ou ")).replace("?", "")
