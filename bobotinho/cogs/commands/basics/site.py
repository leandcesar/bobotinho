# -*- coding: utf-8 -*-
description = "Receba o link do site do Bot para mais informações"
aliases = ["discord", "github", "twitter"]


async def func(ctx):
    ctx.response = f"acesse: {ctx.bot.site}/"
