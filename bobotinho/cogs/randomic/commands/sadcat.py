# -*- coding: utf-8 -*-
aliases = ["sc", "cat"]
description = "Receba a foto de um gatinho triste aleatório"


async def command(ctx):
    sadcat = await ctx.bot.api.sadcat()
    if sadcat:
        ctx.response = f"{sadcat} 😿"
