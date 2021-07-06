# -*- coding: utf-8 -*-
description = "Receba o link para ver o status dos softwares do bot"


async def func(ctx):
    ctx.response = f"veja os status dos softwares: {ctx.bot.site}/status"
