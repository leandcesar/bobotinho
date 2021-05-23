# -*- coding: utf-8 -*-
from bobotinho.database import models
from bobotinho.logger import log
from bobotinho.utils import timetools


async def event_message(bot, message) -> bool:
    # TODO: juntar todos os lembretes que a pessoa tiver em 1 (se não passar de 500 caracteres)
    remind = (
        await models.Reminder.filter(user_to_id=message.author.name, scheduled_for=None)
        .order_by("created_at")
        .first()
    )
    if not remind or "remind" in bot.channels[message.channel.name]["disabled"]:
        return False
    mention = "você" if remind.user_from_id == message.author.name else f"@{remind.user_from_id}"
    content = remind.content or ""
    timeago = timetools.date_in_full(remind.created_ago)
    await remind.delete()
    response = f"@{message.author.name}, {mention} deixou um lembrete: {content} ({timeago})"
    await message.channel.send(response)
    log.debug(f"#{message.channel.name} @{bot.nick}: {response}")
    return True
