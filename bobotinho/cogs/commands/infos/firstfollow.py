# -*- coding: utf-8 -*-
from bobotinho.apis import twitch
from bobotinho.utils import checks, convert

description = "Saiba o primeiro seguidor e o primeiro canal seguido de algum usuário"
aliases = ["ff"]
usage = "digite o comando e o nome de alguém para saber a data de criação da conta"
extra_checks = [checks.banword]


async def func(ctx, arg: str = ""):
    name = convert.str2name(arg, default=ctx.author.name)
    if name == ctx.bot.nick:
        ctx.response = "eu sempre existi..."
    else:
        following = await twitch.TwitchAPI.following(name)
        follower = await twitch.TwitchAPI.followers(name)
        mention = "você" if name == ctx.author.name else f"@{name}"
        if following and "não existe" in following:
            ctx.response = following
        elif following and follower:
            ctx.response = f"{mention} seguiu primeiro @{following} e foi seguido primeiro por @{follower}"
        elif following and not follower:
            ctx.response = f"{mention} seguiu primeiro @{following} e não é seguido por ninguém"
        elif not following and follower:
            ctx.response = f"{mention} não segue ninguém e foi seguido primeiro por @{follower}"
        else:
            ctx.response = f"{mention} não segue e não é seguido por ninguém"
