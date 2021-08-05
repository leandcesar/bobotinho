# -*- coding: utf-8 -*-
from bobotinho.database.models import Channel
from bobotinho.utils import roles

description = "Pause o bot"
extra_checks = [roles.mod]


async def command(ctx):
    ctx.bot.channels[ctx.channel.name]["online"] = False
    await Channel.filter(user_id=ctx.bot.channels[ctx.channel.name]["id"]).update(online=False)
    ctx.response = "você me desligou 💤"
