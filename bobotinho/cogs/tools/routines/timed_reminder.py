# -*- coding: utf-8 -*-
import asyncio
from datetime import timedelta

from bobotinho.database.models import Reminder
from bobotinho.database.base import timezone
from bobotinho import log
from bobotinho.utils import timetools

delta = 60


async def routine(bot) -> None:
    now = timezone.now()
    reminds = await Reminder.filter(
        scheduled_for__not_isnull=True,
        scheduled_for__lt=now + timedelta(seconds=60),
    ).order_by("scheduled_for").all()
    for remind in reminds:
        await remind.fetch_related("from_user", "to_user", "channel")
        mention = "você" if remind.from_user_id == remind.to_user_id else f"@{remind.from_user.name}"
        content = remind.content or ""
        await remind.delete()
        if (
            "remind" not in bot.channels[remind.channel.name]["disabled"]
            and bot.channels[remind.channel.name]["online"]
            and not any(x in content for x in bot.channels[remind.channel.name]["banwords"])
        ):
            if (delta := remind.scheduled_ago.total_seconds()) > 0:
                await asyncio.sleep(delta, loop=bot.loop)
            timeago = timetools.date_in_full(remind.created_ago)
            response = f"{remind.to_user.name}, {mention} deixou um lembrete cronometrado: {content} ({timeago})"
            try:
                await bot.get_channel(remind.channel.name).send(response)
                log.info(f"#{remind.channel.name} @{bot.nick}: {response}")
            except Exception as e:
                log.exception(e)
