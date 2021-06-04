# -*- coding: utf-8 -*-
description = "Receba o link das novidades de atualizações do bot"


async def func(ctx):
    ctx.response = f"veja as últimas atualizações: {ctx.bot.site}/blog/tags/news"
