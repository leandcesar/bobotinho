# -*- coding: utf-8 -*-
from bobotinho.cogs.tools import afks
from bobotinho.database import Afk, User
from bobotinho.utils import convert, timetools

description = "Verifique se alguém está AFK"
usage = "digite o comando e o nome do usuário para saber se ele está AFK"


async def command(ctx, arg: str):
    name = convert.str2name(arg)
    if name == ctx.bot.nick:
        ctx.response = "eu sempre estou aqui... observando"
    elif name == ctx.author.name:
        ctx.response = "você não está AFK... obviamente"
    elif not (user := await User.get_or_none(name=name)):
        ctx.response = f"@{name} ainda não foi registrado (não usou nenhum comando)"
    elif not user.mention:
        ctx.response = "esse usuário optou por não permitir mencioná-lo"
    elif (afk := await Afk.get_or_none(user_id=user.id)):
        afk_type = afks[afk.alias]
        timesince = timetools.date_in_full(afk.created_ago)
        ctx.response = f"@{name} está {afk_type.isafk}: {afk.content or afk_type.emoji} ({timesince})"
    else:
        ctx.response = f"@{name} não está AFK"
