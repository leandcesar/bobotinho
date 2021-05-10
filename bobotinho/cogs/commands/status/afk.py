# -*- coding: utf-8 -*-
from bobotinho.cogs.commands.status import afks
from bobotinho.database import models
from bobotinho.utils import checks

description = "Informe que você está se ausentando do chat"
aliases = list(afks.keys())[1:]
extra_checks = [checks.is_allowed, checks.is_banword]


async def func(ctx, *, content: str = ""):
    if content and len(content) > 400:
        ctx.response = "essa mensagem é muito comprida"
    else:
        if await models.Afk.exists(user_id=ctx.author.name):
            await models.Afk.filter(user_id=ctx.author.name).delete()
        afk_type = afks[ctx.command.invocation]
        await models.Afk.update_or_create(
            user_id=ctx.author.name,
            alias=ctx.command.invocation,
            status=True,
            content=content,
        )
        ctx.response = f"você {afk_type.afk}: {content or afk_type.emoji}"
