# -*- coding: utf-8 -*-
description = "Receba o link das notas de atualização do bot"
aliases = ["pn"]


async def func(ctx):
    ctx.response = f"veja as notas de atualização: {ctx.bot.site}/patch-notes"
