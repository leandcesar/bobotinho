# -*- coding: utf-8 -*-
from bobotinho.database import models
from bobotinho.utils import timetools

description = "Verifique há quanto tempo o bot está online"


async def func(ctx):
    uptime = await models.SystemLog.filter().order_by("-id").first()
    timesince = timetools.date_in_full(uptime.created_ago)
    ctx.response = f"{timesince} desde a última inicialização"
