# -*- coding: utf-8 -*-
import random

from bobotinho.utils import checks

description = "Sorteia uma palavra da mensagem informada"
usage = "digite o comando e opções separadas por espaço"
extra_checks = [checks.is_banword]


async def func(ctx, *, content: str):
    ctx.response = random.choice(content.replace(",", "").split())
