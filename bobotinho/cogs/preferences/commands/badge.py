# -*- coding: utf-8 -*-
from bobotinho.utils import convert

description = "Defina a sua badge de apoiador"
usage = "digite o comando e um emoji que quiser usar como badge"
extra_checks = ["Role.sponsor"]


async def command(ctx, arg: str):
    if arg == "remove":
        ctx.user.badge = ""
        await ctx.user.save()
        ctx.response = "você removeu sua badge de apoiador"
    elif badge := convert.emoji2str(arg):
        ctx.user.badge = badge
        await ctx.user.save()
        ctx.response = "você alterou sua badge de apoiador"
