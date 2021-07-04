# -*- coding: utf-8 -*-
import re

from bobotinho.utils import roles


class BotIsNotOnline(Exception):
    pass


class ContentHasBanword(Exception):
    pass


class CommandIsDisabled(Exception):
    pass


class CommandIsOnCooldown(Exception):
    pass


class UserIsNotAllowed(Exception):
    pass


def allowed(ctx) -> bool:
    if not roles.any(ctx) and re.search(r"([0-9a-zA-Z]*\.[a-zA-Z]{2,3})", ctx.content) is not None:
        raise UserIsNotAllowed()
    return True


def banword(ctx) -> bool:
    if any(word in ctx.content for word in ctx.bot.channels[ctx.channel.name]["banwords"]):
        raise ContentHasBanword()
    return True


def cooldown(ctx) -> bool:
    if not ctx.bot.cooldowns.set(f"{ctx.author.id}-{ctx.command.name}", 1, ex=5, nx=True):
        raise CommandIsOnCooldown()
    return True


def enabled(ctx) -> bool:
    if ctx.command.name in ctx.bot.channels[ctx.channel.name]["disabled"]:
        raise CommandIsDisabled()
    return True


def online(ctx) -> bool:
    if not ctx.bot.channels[ctx.channel.name]["online"]:
        raise BotIsNotOnline()
    return True
