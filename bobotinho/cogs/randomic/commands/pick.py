# -*- coding: utf-8 -*-
import random

description = "Sorteia uma palavra da mensagem informada"
usage = "digite o comando e opções separadas por espaço"


async def command(ctx, *, content: str):
    ctx.response = random.choice(content.replace(",", "").split())
