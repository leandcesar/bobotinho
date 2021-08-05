# -*- coding: utf-8 -*-
from bobotinho.utils import convert, roles

description = "Defina a sua badge de apoiador"
usage = "digite o comando e um emoji que quiser usar como badge"
extra_checks = [roles.sponsor]


async def command(ctx, arg: str):
    emoji = convert.emoji2str(arg)
    if emoji != arg and emoji.count(":") == 2:
        ctx.user.badge = arg
        await ctx.user.save()
        ctx.response = "você alterou sua badge de apoiador"
