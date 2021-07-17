# -*- coding: utf-8 -*-
import asyncio

from bobotinho.cogs.tasks import send_message
from bobotinho.database import models
from bobotinho.utils import timetools


async def func(bot) -> None:
    # TODO: substituir pra quando o bot iniciar pegar os proximos,
    #       mas depois pegar os novos reminds por trigger
    while True:
        remind = await models.Reminder.filter(scheduled_for__not_isnull=True).order_by("scheduled_for").first()
        if not remind or (delta := remind.scheduled_ago.total_seconds()) > 60:
            await asyncio.sleep(60, loop=bot.loop)
            continue
        if delta > 0:
            await asyncio.sleep(delta, loop=bot.loop)
        from_user = await models.User.get(id=remind.from_user_id)
        channel = await models.User.get(id=remind.channel_id)
        if remind.from_user_id == remind.to_user_id:
            to_user = from_user
            mention = "você"
        else:
            to_user = await models.User.get(id=remind.to_user_id)
            mention = f"@{from_user.name}"
        content = remind.content or ""
        timeago = timetools.date_in_full(remind.created_ago)
        response = f"{to_user}, {mention} deixou um lembrete cronometrado: {content} ({timeago})"
        await remind.delete()
        if "remind" not in bot.channels[channel.name]["disabled"]:
            await send_message(bot, channel.name, response)
