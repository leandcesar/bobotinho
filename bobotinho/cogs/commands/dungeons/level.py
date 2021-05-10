# -*- coding: utf-8 -*-
from bobotinho.cogs.commands.dungeons import classes
from bobotinho.database import models
from bobotinho.utils import checks, convert

description = "Veja qual o seu level (ou de alguém) e outras estatísticas da dungeon"
aliases = ["lvl"]
extra_checks = [checks.is_banword]


async def func(ctx, arg: str = ""):
    name = convert.str2username(arg) or ctx.author.name
    mention = "você" if name == ctx.author.name else f"@{name}"
    if not name:
        ctx.response = "nome de usuário inválido"
    elif name == ctx.bot.nick:
        ctx.response = "eu apenas crio as dungeons..."
    elif dungeon := await models.Dungeon.get_or_none(user_id=name):
        if not dungeon.sub_class:
            ctx.response = f"{mention} ainda não escolheu a nova classe"
        else:
            total = (dungeon.wins + dungeon.defeats)
            winrate = dungeon.wins / (total or 1) * 100
            sub_class = classes[dungeon.class_][dungeon.gender][dungeon.sub_class][dungeon.level // 10]
            ctx.response = (
                f"{mention} é {sub_class} ({dungeon.level}, {dungeon.xp} XP) com {total} dungeons "
                f"({dungeon.wins} vitórias, {dungeon.defeats} derrotas, {winrate:.2f}% winrate) ♦"
            )
    else:
        ctx.response = f"{mention} ainda não entrou em nenhuma dungeon"
