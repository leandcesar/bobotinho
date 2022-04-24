# -*- coding: utf-8 -*-
from bobotinho.utils import convert

FILENAME = "bobotinho//data//jokes.txt"
aliases = ["4head", "hahaa"]
description = "Receba uma piada ou trocadilho aleatório"


async def command(ctx):
    joke = await ctx.bot.api.joke()
    if joke:
        ctx.response = f"{joke} 4Head"
