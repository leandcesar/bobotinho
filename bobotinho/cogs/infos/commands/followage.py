# -*- coding: utf-8 -*-
from bobotinho.utils import convert, timetools

description = "Saiba há quanto tempo algum usuário segue algum canal"
aliases = ["fa"]


async def command(ctx, arg1: str = "", arg2: str = ""):
    name = convert.str2name(arg1, default=ctx.author.name)
    channel = convert.str2name(arg2, default=ctx.channel.name)
    if name and channel:
        data = await ctx.bot.api.twitch("follow_age", channel, name)
        name = "você" if name == ctx.author.name else f"@{name}"
        channel = "você" if channel == ctx.author.name else f"@{channel}"
    if name == f"@{ctx.bot.nick}":
        ctx.response = f"eu sempre estive em {channel}..."
    elif name == channel:
        ctx.response = f"{name} não pode se seguir"
    elif data and data["follow_age"] and not "não segue" in data["follow_age"]:
        follow_age = data["follow_age"]
        ctx.response = f"{name} segue {channel} há {follow_age}"
    else:
        ctx.response = f"{name} não segue {channel}"
