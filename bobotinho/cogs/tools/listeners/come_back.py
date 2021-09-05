# -*- coding: utf-8 -*-
from bobotinho.cogs.tools import afks
from bobotinho.database.models import Afk
from bobotinho.utils import convert, timetools


async def listener(ctx) -> None:
    if afk := await Afk.get_or_none(user_id=ctx.author.id):
        action = afks[afk.alias].returned
        content = afk.content or afks[afk.alias].emoji
        timeago = timetools.date_in_full(afk.created_ago)
        await afk.delete()
        timestamp = convert.datetime2str(afk.created_at)
        afk = convert.dict2str({"content": content, "created_at": timestamp})
        ctx.bot.cache.set(f"afk-{ctx.author.id}", afk, ex=180)
        if "afk" not in ctx.bot.channels[ctx.channel.name]["disabled"]:
            ctx.response = f"você {action}: {content} ({timeago})"
