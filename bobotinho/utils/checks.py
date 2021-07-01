# -*- coding: utf-8 -*-
import time
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
    ctx.bot.cooldowns = {
        k: v
        for k, v in ctx.bot.cooldowns.items()
        if v > time.monotonic()
    }
    if len(ctx.bot.cooldowns) > 512:
        ctx.bot.cooldowns = {}  # TODO: não fazer isso
    if ctx.bot.cooldowns.get(f"{ctx.author.id}-{ctx.command.name}"):
        raise CommandIsOnCooldown()
    ctx.bot.cooldowns[f"{ctx.author.id}-{ctx.command.name}"] = time.monotonic() + 5
    return True


def enabled(ctx) -> bool:
    if ctx.command.name in ctx.bot.channels[ctx.channel.name]["disabled"]:
        raise CommandIsDisabled()
    return True


def online(ctx) -> bool:
    if not ctx.bot.channels[ctx.channel.name]["status"]:
        raise BotIsNotOnline()
    return True
