# -*- coding: utf-8 -*-
description = "Receba o link para apoiar o bot"
aliases = ["pix", "paypal", "picpay"]


async def command(ctx):
    ctx.response = f"me ajude a continuar vivo! {ctx.bot.site}/donate"
