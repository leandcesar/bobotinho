# -*- coding: utf-8 -*-
from bobotinho.database.models import User, Wedding
from bobotinho.utils import convert, timetools

description = "Saiba há quanto tempo algum usuário está casado"
aliases = ["ma"]


async def command(ctx, arg: str = ""):
    name = convert.str2name(arg, default=ctx.author.name)
    mention = "você" if name == ctx.author.name else f"@{name}"
    if name == ctx.bot.nick:
        ctx.response = "nunca me casarei com ninguém"
    elif not (user := await User.get_or_none(name=name)):
        ctx.response = f"@{name} ainda não foi registrado (não usou nenhum comando)"
    elif arg and not user.mention:
        ctx.response = "esse usuário optou por não permitir mencioná-lo"
    elif (weddings := await Wedding.find_all(user.id)):
        users = [await wedding.spouse(name) for wedding in weddings]
        timeago = [timetools.timeago(wedding.created_at) for wedding in weddings]
        if len(weddings) == 1:
            ctx.response = f"{mention} está casado com @{users[0].name} há {timeago[0]}"
        else:
            ctx.response = (
                f"{mention} está casado com @{users[0].name} há {timeago[0]} e "
                f"com @{users[1].name} há {timeago[1]}"
            )
    else:
        ctx.response = f"{mention} não está casado com ninguém"
