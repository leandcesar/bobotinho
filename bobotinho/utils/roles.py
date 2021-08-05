# -*- coding: utf-8 -*-

def owner(ctx) -> bool:
    return ctx.author.name == ctx.bot.owner


def streamer(ctx) -> bool:
    return ctx.author.name == ctx.channel.name


def mod(ctx) -> bool:
    return ctx.author.is_mod or streamer(ctx) or owner(ctx)


def vip(ctx) -> bool:
    return bool(ctx.author.badges.get("vip"))


def sub(ctx) -> bool:
    return ctx.author.is_subscriber


def any(ctx) -> bool:
    return sub(ctx) or vip(ctx) or mod(ctx) or streamer(ctx) or owner(ctx)


def sponsor(ctx) -> bool:
    return ctx.user and ctx.user.sponsor
