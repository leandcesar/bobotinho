# -*- coding: utf-8 -*-
description = "Saiba as novidades e atualizações do bot"


async def command(ctx):
    ctx.response = f"para acompanhar as novidades, entre no servidor do Discord: {ctx.bot.site}/"
