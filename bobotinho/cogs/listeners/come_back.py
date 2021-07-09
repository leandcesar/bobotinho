# -*- coding: utf-8 -*-
from bobotinho.cogs.commands.status import afks
from bobotinho.database import models
from bobotinho.logger import log
from bobotinho.utils import convert, timetools


async def event_message(bot, message) -> bool:
    if afk := await models.Afk.get_or_none(user_id=message.author.id):
        action = afks[afk.alias].returned
        content = afk.content or afks[afk.alias].emoji
        timeago = timetools.date_in_full(afk.created_ago)
        await afk.delete()
        timestamp = convert.datetime2str(afk.created_at)
        afk = convert.dict2str({"content": content, "created_at": timestamp})
        bot.cache.set(f"afk-{message.author.id}", afk, ex=180)
        if "afk" not in bot.channels[message.channel.name]["disabled"]:
            user = await models.User.get(id=message.author.id)
            response = f"{user} {action}: {content} ({timeago})"
            await message.channel.send(response)
            log.debug(f"#{message.channel.name} @{bot.nick}: {response}")
            return True
    return False
