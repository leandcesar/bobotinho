# -*- coding: utf-8 -*-
import asyncio
from datetime import timedelta

from bobotinho.database import Reminder
from bobotinho.database.base import timezone
from bobotinho import log
from bobotinho.utils import timetools

delta = 60


async def routine(bot) -> None:
    reminds = await Reminder.filter(
        scheduled_for__not_isnull=True,
        scheduled_for__lt=timezone.now() + timedelta(seconds=60),
        channel_id__in=[channel["id"] for channel in bot.channels.values()]
    ).order_by("scheduled_for").all()
    for remind in reminds:
        await remind.fetch_related("from_user", "to_user", "channel")
        mention = "você" if remind.from_user_id == remind.to_user_id else f"@{remind.from_user.name}"
        content = remind.content or ""
        channel = remind.channel.name
        await remind.delete()
        if (
            "remind" not in bot.channels[channel]["disabled"]
            and bot.channels[channel]["online"]
            and not any(x in content for x in bot.channels[channel]["banwords"])
        ):
            delta = remind.scheduled_to.total_seconds()
            if delta > 0:
                await asyncio.sleep(delta, loop=bot.loop)
            timeago = timetools.date_in_full(remind.created_ago)
            response = f"{remind.to_user}, {mention} deixou um lembrete cronometrado: {content} ({timeago})"
            try:
                await bot.create_user(remind.channel.id, remind.channel.name).channel.send(response)
                log.info(f"#{channel} @{bot.nick}: {response}")
            except Exception as e:
                log.exception(e, extra={"locals": locals()})
