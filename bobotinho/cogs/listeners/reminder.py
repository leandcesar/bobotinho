# -*- coding: utf-8 -*-
from bobotinho.database import models
from bobotinho.logger import log
from bobotinho.utils import timetools


async def event_message(bot, message) -> bool:
    # TODO: juntar todos os lembretes que a pessoa tiver em 1 (se não passar de 500 caracteres)
    remind = (
        await models.Reminder.filter(to_user_id=message.author.id, scheduled_for=None)
        .order_by("created_at")
        .first()
    )
    if not remind or "remind" in bot.channels[message.channel.name]["disabled"]:
        return False
    from_user = await models.User.get_or_none(id=remind.from_user_id)
    to_user = await models.User.get_or_none(id=remind.to_user_id)
    mention = "você" if remind.from_user_id == message.author.id else f"@{from_user.name}"
    content = remind.content or ""
    timeago = timetools.date_in_full(remind.created_ago)
    await remind.delete()
    response = f"{to_user}, {mention} deixou um lembrete: {content} ({timeago})"
    await message.channel.send(response)
    log.debug(f"#{message.channel.name} @{bot.nick}: {response}")
    return True
