# -*- coding: utf-8 -*-
from bobotinho.database.models import Channel

description = "Despause o bot"
extra_checks = ["Role.admin"]
no_global_checks = True


async def command(ctx):
    if ctx.bot.channels[ctx.channel.name]["online"]:
        ctx.response = "já estou ligado ☕"
    else:
        ctx.bot.channels[ctx.channel.name]["online"] = True
        await Channel.filter(user_id=ctx.bot.channels[ctx.channel.name]["id"]).update(online=True)
        ctx.response = "você me ligou ☕"
