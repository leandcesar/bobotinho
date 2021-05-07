# -*- coding: utf-8 -*-
import time

from bobotinho.utils import checks, convert

description = "Desafie um usuário para lutar"
usage = "digite o comando e o nome de alguém para desafiá-lo para luta"
extra_checks = [checks.is_banword]


async def func(ctx, arg: str):
    ctx.bot.cache["fights"] = {
        k: v
        for k, v in ctx.bot.cache.get("fights", {}).items()
        if v["time"] > time.monotonic()
    }
    name = convert.str2username(arg)
    if not name:
        ctx.response = "nome de usuário inválido"
    elif name == ctx.bot.nick:
        ctx.response = "você não conseguiria me derrotar..."
    elif name == ctx.author.name:
        ctx.response = "você iniciou uma luta interna... FeelsBadMan"
    elif ctx.author.name in ctx.bot.cache["fights"].keys():
        ctx.response = (
            "você já está sendo desafiado por alguém, "
            f'digite "{ctx.prefix}accept" ou "{ctx.prefix}deny"'
        )
    elif any([v for v in ctx.bot.cache["fights"].values() if ctx.author.name == v["name"]]):
        ctx.response = f'você já desafiou alguém, digite "{ctx.prefix}cancel" para cancelar'
    elif name in ctx.bot.cache["fights"].keys():
        ctx.response = f"@{name} já está sendo desafiado por alguém"
    elif any([v for v in ctx.bot.cache["fights"].values() if name == v["name"]]):
        ctx.response = f"@{name} já está desafiando alguém"
    else:
        ctx.bot.cache["fights"][name] = {"name": ctx.author.name, "time": time.monotonic() + 60}
        ctx.response = (
            f"você desafiou @{name}, aguarde o usuário "
            f'digitar "{ctx.prefix}accept" ou "{ctx.prefix}deny"'
        )
