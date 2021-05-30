# -*- coding: utf-8 -*-
from bobotinho.cogs.commands.status import afks
from bobotinho.database import models

description = "Retome seu status de ausência do chat"
aliases = [f"r{alias}" for alias in list(afks.keys())[1:]]
usage = "digite o comando em até 3 minutos após ter retornado do seu AFK para retomá-lo"


async def func(ctx):
    if afk := await models.Afk.get_or_none(user_id=ctx.author.id):
        afk.status = True
        await afk.save()
        afk_type = afks[afk.alias]
        ctx.response = f"você continuou {afk_type.rafk}: {afk.content or afk_type.emoji}"
