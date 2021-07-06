# -*- coding: utf-8 -*-
from bobotinho.cogs.commands.status import afks
from bobotinho.database import models
from bobotinho.utils import checks

description = "Informe que você está se ausentando do chat"
aliases = list(afks.keys())[1:]
extra_checks = [checks.allowed, checks.banword]


async def func(ctx, *, content: str = ""):
    if content and len(content) > 400:
        ctx.response = "essa mensagem é muito comprida"
    else:
        afk_type = afks[ctx.command.invocation]
        await models.Afk.create(
            user_id=ctx.author.id,
            alias=ctx.command.invocation,
            content=content,
        )
        ctx.response = f"você {afk_type.afk}: {content or afk_type.emoji}"
