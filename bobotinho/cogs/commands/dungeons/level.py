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
    elif player := await models.Player.get_or_none(name=name):
        if not player.sub_class:
            ctx.response = f"{mention} ainda não escolheu a nova classe"
        else:
            total = (player.wins + player.defeats)
            winrate = player.wins / (total or 1) * 100
            lvl = player.level // 10 if player.level < 60 else 6
            sub_class = classes[player.class_][player.gender][player.sub_class][lvl]
            ctx.response = (
                f"{mention} é {sub_class} ({player.level}, {player.xp} XP) com {total} dungeons "
                f"({player.wins} vitórias, {player.defeats} derrotas, {winrate:.2f}% winrate) ♦"
            )
    else:
        ctx.response = f"{mention} ainda não entrou em nenhuma dungeon"
