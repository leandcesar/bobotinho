# -*- coding: utf-8 -*-
from bobotinho.utils import checks, convert

description = "Desafie um usuário para lutar"
usage = "digite o comando e o nome de alguém para desafiá-lo para luta"
extra_checks = [checks.banword]


async def func(ctx, arg: str):
    name = convert.str2username(arg)
    if not name:
        ctx.response = "nome de usuário inválido"
    elif name == ctx.bot.nick:
        ctx.response = "você não conseguiria me derrotar..."
    elif name == ctx.author.name:
        ctx.response = "você iniciou uma luta interna... FeelsBadMan"
    elif someone := ctx.bot.cache.get(f"fight-{ctx.author.name}"):
        ctx.response = (
            f"você já está sendo desafiado por @{someone}, "
            f'digite "{ctx.prefix}accept" ou "{ctx.prefix}deny"'
        )
    elif someone := ctx.bot.cache.get(f"fight-{name}"):
        ctx.response = f"@{name} já está sendo desafiado por @{someone}"
    else:
        ctx.bot.cache.set(f"fight-{name}", ctx.author.name, ex=60)
        ctx.response = (
            f"você desafiou @{name}, aguarde o usuário "
            f'digitar "{ctx.prefix}accept" ou "{ctx.prefix}deny"'
        )
