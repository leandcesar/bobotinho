# -*- coding: utf-8 -*-
import random

from bobotinho.apis import Color
from bobotinho.database.models import User
from bobotinho.utils import convert

description = "Saiba o código hexadecimal da cor de algum usuário"
aliases = ["colour"]


async def command(ctx, arg: str = ""):
    name = convert.str2name(arg, default=ctx.author.name)
    if name == ctx.bot.nick:
        ctx.response = "eu uso a cor #FFFFFF (White)"
    elif name == "random":
        ctx.response = f"aqui está uma cor aleatória: #{random.randint(0, 0xFFFFFF):06X}"
    elif not (user := await User.get_or_none(name=name)):
        ctx.response = f"@{name} ainda não foi registrado (não usou nenhum comando)"
    elif arg and not user.mention:
        ctx.response = "esse usuário optou por não permitir mencioná-lo"
    else:
        mention = "você" if name == ctx.author.name else f"@{name}"
        ctx.response = f"{mention} usa a cor {user.color}"
        if color_name := await Color.name(user.color[1:]):
            ctx.response += f" ({color_name})"
        if user.saved_color:
            ctx.response += f" e salvou a cor {user.saved_color}"
