# -*- coding: utf-8 -*-
from bobotinho.cogs.status import afks
from bobotinho.database.models import Afk
from bobotinho.utils import convert

description = "Retome seu status de ausência do chat"
aliases = [f"r{alias}" for alias in list(afks.keys())[1:]]
usage = "digite o comando em até 3 minutos após ter retornado do seu AFK para retomá-lo"


async def command(ctx):
    if afk := ctx.bot.cache.get(f"afk-{ctx.author.id}"):
        ctx.bot.cache.delete(f"afk-{ctx.author.id}")
        invoke_by = ctx.message.content.partition(" ")[0][len(ctx.prefix):].lower()
        afk_type = afks[invoke_by[1:]]
        afk = convert.str2dict(afk)
        content = afk.get("content")
        created_at = convert.str2datetime(afk.get("created_at"))
        await Afk.create(
            user_id=ctx.author.id,
            alias=invoke_by[1:],
            content=content,
            created_at=created_at,
        )
        ctx.response = f"você continuou {afk_type.rafk}: {content or afk_type.emoji}"
