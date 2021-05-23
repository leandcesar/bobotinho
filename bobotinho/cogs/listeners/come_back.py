# -*- coding: utf-8 -*-
from bobotinho.cogs.commands.status import afks
from bobotinho.database import models
from bobotinho.logger import log
from bobotinho.utils import timetools


async def event_message(bot, message) -> bool:
    if afk := await models.Afk.get_or_none(user_id=message.author.name, status=True):
        action = afks[afk.alias].returned
        content = afk.content or afks[afk.alias].emoji
        timeago = timetools.date_in_full(afk.created_ago)
        afk.status = False
        await afk.save()
        if "afk" not in bot.channels[message.channel.name]["disabled"]:
            response = f"{message.author.name} {action}: {content} ({timeago})"
            await message.channel.send(response)
            log.debug(f"#{message.channel.name} @{bot.nick}: {response}")
            return True
    return False
