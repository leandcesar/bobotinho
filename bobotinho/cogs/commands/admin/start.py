# -*- coding: utf-8 -*-
from bobotinho.database import models
from bobotinho.utils import roles

description = "Despause o bot"
extra_checks = [roles.mod]
no_global_checks = True


async def func(ctx):
    if ctx.bot.channels[ctx.channel.name]["status"]:
        ctx.response = "já estou ligado ☕"
    else:
        ctx.bot.channels[ctx.channel.name]["status"] = True
        await models.Channel.filter(user_id=ctx.bot.channels[ctx.channel.name]["id"]).update(status=True)
        ctx.response = "você me ligou ☕"
