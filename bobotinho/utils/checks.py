# -*- coding: utf-8 -*-
import time
import re


def is_streamer(ctx) -> bool:
    return ctx.author.name == ctx.channel.name


def is_mod(ctx) -> bool:
    return ctx.author.is_mod or is_streamer(ctx)


def is_vip(ctx) -> bool:
    return bool(ctx.author.badges.get("vip"))


def is_sub(ctx) -> bool:
    return ctx.author.is_subscriber


def is_banword(ctx) -> bool:
    print(ctx.bot.channels[ctx.channel.name]["banwords"])
    return not any(x in ctx.content for x in ctx.bot.channels[ctx.channel.name]["banwords"])


def is_cooldown(ctx) -> bool:
    ctx.bot.cooldowns = {
        k: v
        for k, v in ctx.bot.cooldowns.items()
        if v > time.monotonic()
    }
    on_cooldown = ctx.bot.cooldowns.get(f"{ctx.author.id}-{ctx.command.name}")
    if not on_cooldown:
        ctx.bot.cooldowns[f"{ctx.author.id}-{ctx.command.name}"] = time.monotonic() + 5
    return not on_cooldown


def is_enabled(ctx) -> bool:
    return ctx.command.name not in ctx.bot.channels[ctx.channel.name]["disabled"]


def is_online(ctx) -> bool:
    return ctx.bot.channels[ctx.channel.name]["status"]


def is_link(ctx) -> bool:
    return re.search(r"([0-9a-zA-Z]*\.[a-zA-Z]{2,3})", ctx.content) is not None


def is_allowed(ctx) -> bool:
    return is_sub(ctx) or is_vip(ctx) or is_mod(ctx) or is_streamer(ctx) or not is_link(ctx)
