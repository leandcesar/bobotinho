# -*- coding: utf-8 -*-
description = "Receba o link para adicionar o bot no seu chat"


async def func(ctx):
    ctx.response = f"me adicione no seu chat: {ctx.bot.site}/invite"
