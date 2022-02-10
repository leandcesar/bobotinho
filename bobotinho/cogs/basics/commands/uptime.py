# -*- coding: utf-8 -*-
from bobotinho.utils import timetools

description = "Verifique há quanto tempo o bot está online"


async def command(ctx):
    timesince = timetools.date_in_full(ctx.bot.boot_ago)
    ctx.response = f"{timesince} desde a última inicialização"
