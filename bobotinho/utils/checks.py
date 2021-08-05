# -*- coding: utf-8 -*-
import re

from bobotinho.utils import roles
from bobotinho.exceptions import (
    BotIsOffline,
    ContentHasBanword,
    CommandIsDisabled,
    UserIsNotAllowed,
)


def allowed(ctx) -> bool:
    if not roles.any(ctx) and re.search(r"([0-9a-zA-Z]*\.[a-zA-Z]{2,3})", ctx.message.content) is not None:
        raise UserIsNotAllowed(channel=ctx.channel.name, user=ctx.author.name)
    return True


def banword(ctx) -> bool:
    if any(word in ctx.message.content for word in ctx.bot.channels[ctx.channel.name]["banwords"]):
        raise ContentHasBanword(channel=ctx.channel.name, content=ctx.message.content)
    return True


def enabled(ctx) -> bool:
    if ctx.command.name in ctx.bot.channels[ctx.channel.name]["disabled"]:
        raise CommandIsDisabled(channel=ctx.channel.name, command=ctx.command.name)
    return True


def online(ctx) -> bool:
    if not ctx.bot.channels[ctx.channel.name]["online"]:
        raise BotIsOffline(channel=ctx.channel.name)
    return True
