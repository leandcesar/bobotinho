# -*- coding: utf-8 -*-
from bobotinho.database import models
from bobotinho.utils import roles

description = "Pause o bot"
extra_checks = [roles.mod]


async def func(ctx):
    ctx.bot.channels[ctx.channel.name]["online"] = False
    await models.Channel.filter(user_id=ctx.bot.channels[ctx.channel.name]["id"]).update(online=False)
    ctx.response = "você me desligou 💤"
