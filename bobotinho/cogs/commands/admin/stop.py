# -*- coding: utf-8 -*-
from bobotinho.database import models
from bobotinho.utils import checks

description = "Pause o bot"
extra_checks = [checks.is_mod]


async def func(ctx):
    ctx.bot.channels[ctx.channel.name]["status"] = False
    await models.Channel.filter(user_id=ctx.channel.name).update(status=False)
    ctx.response = "você me desligou 💤"
