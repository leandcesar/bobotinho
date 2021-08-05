# -*- coding: utf-8 -*-
from bobotinho.database.models import Reminder, User
from bobotinho.utils import timetools


async def listener(ctx) -> None:
    # TODO: juntar todos os lembretes que a pessoa tiver em 1 (se não passar de 500 caracteres)
    remind = (
        await Reminder.filter(to_user_id=ctx.author.id, scheduled_for=None)
        .order_by("created_at")
        .first()
    )
    if not remind or "remind" in ctx.bot.channels[ctx.channel.name]["disabled"]:
        return False
    from_user = await User.get_or_none(id=remind.from_user_id)
    mention = "você" if remind.from_user_id == ctx.author.id else f"@{from_user.name}"
    content = remind.content or ""
    timeago = timetools.date_in_full(remind.created_ago)
    await remind.delete()
    ctx.response = f"{mention} deixou um lembrete: {content} ({timeago})"
