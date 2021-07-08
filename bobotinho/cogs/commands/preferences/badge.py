# -*- coding: utf-8 -*-
from bobotinho.utils import checks, convert

description = "Defina a sua badge de apoiador"
usage = 'digite o comando e o emoji que quiser usar como badge no bot'
extra_checks = [checks.sponsor]


async def func(ctx, arg: str):
    if convert.emoji2str(arg) != arg:
        ctx.user.badge = arg
        await ctx.user.save()
        ctx.response = "você alterou sua badge de apoiador"
