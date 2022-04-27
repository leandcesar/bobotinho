# -*- coding: utf-8 -*-
from bobotinho.utils import convert, timetools

description = "Saiba há quanto tempo algum usuário criou sua conta"
aliases = ["age"]
usage = "digite o comando e o nome de alguém para saber a data de criação da conta"


async def command(ctx, arg: str = ""):
    name = convert.str2name(arg, default=ctx.author.name)
    if name == ctx.bot.nick:
        ctx.response = "eu sempre existi..."
    else:
        mention = "você" if name == ctx.author.name else f"@{name}"
        data = await ctx.bot.api.twitch("account_age", name)
        if data and data["account_age"]:
            account_age = data["account_age"]
            ctx.response = f"{mention} criou a conta há {account_age}"
        else:
            ctx.response = f"{mention} não existe"
