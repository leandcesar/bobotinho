# -*- coding: utf-8 -*-
from bobotinho.database.models import SystemLog
from bobotinho.utils import timetools

description = "Verifique há quanto tempo o bot está online"


async def command(ctx):
    uptime = await SystemLog.filter().order_by("-id").first()
    timesince = timetools.date_in_full(uptime.created_ago)
    ctx.response = f"{timesince} desde a última inicialização"
