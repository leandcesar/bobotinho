# -*- coding: utf-8 -*-
from bobotinho.cogs.commands.status import afks
from bobotinho.database import models
from bobotinho.utils import checks, convert, timetools

description = "Verifique se alguém está AFK"
usage = "digite o comando e o nome do usuário para saber se ele está AFK"
extra_checks = [checks.is_banword]


async def func(ctx, arg: str):
    name = convert.str2username(arg)
    if not name:
        ctx.response = "nome de usuário inválido"
    elif name == ctx.bot.nick:
        ctx.response = "eu sempre estou aqui... observando"
    elif name == ctx.author.name:
        ctx.response = "você não está AFK... obviamente"
    elif not (user := await models.User.get_or_none(name=name)):
        ctx.response = f"@{name} ainda não foi registrado (não usou nenhum comando)"
    elif (afk := await models.Afk.get_or_none(user_id=user.id)) and afk.status:
        afk_type = afks[afk.alias]
        timesince = timetools.date_in_full(afk.created_ago)
        ctx.response = f"@{name} está {afk_type.isafk}: {afk.content or afk_type.emoji} ({timesince})"
    else:
        ctx.response = f"@{name} não está AFK"
