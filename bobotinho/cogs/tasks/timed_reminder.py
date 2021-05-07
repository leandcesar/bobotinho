# -*- coding: utf-8 -*-
import asyncio

from bobotinho.database import models
from bobotinho.cogs.tasks import send_message
from bobotinho.utils import timetools


async def func(bot):
    # TODO: substituir pra quando o bot iniciar pegar os proximos,
    #       mas depois pegar os novos reminds por trigger
    while True:
        remind = await models.Reminder.filter().order_by("scheduled_for").first()
        if not remind or (delta := await remind.scheduled_ago) > 60:
            await asyncio.sleep(60, loop=bot.loop)
            continue
        if delta > 0:
            await asyncio.sleep(delta, loop=bot.loop)
        mention = "você" if remind.user_from_id == remind.user_to_id else f"@{remind.user_from_id}"
        content = remind.content or ""
        timeago = timetools.timeago(remind.created_at)
        response = f"@{remind.user_to_id}, {mention} deixou um lembrete cronometrado: {content} ({timeago})"
        await remind.delete()
        if "remind" not in bot.channels[remind.channel_id]["disabled"]:
            await send_message(bot, remind.channel_id, response)
