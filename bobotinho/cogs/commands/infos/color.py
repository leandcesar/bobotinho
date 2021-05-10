# -*- coding: utf-8 -*-
import random

from bobotinho.apis import color
from bobotinho.database import models
from bobotinho.utils import checks, convert

description = "Saiba o código hexadecimal da cor de algum usuário"
aliases = ["colour"]
extra_checks = [checks.is_banword]


async def func(ctx, arg: str = ""):
    name = convert.str2username(arg) or ctx.author.name
    if not name:
        ctx.response = "nome de usuário inválido"
    elif name == ctx.bot.nick:
        ctx.response = "eu uso a cor #FFFFFF (White)"
    elif name == "random":
        ctx.response = f"aqui está uma cor aleatória: #{random.randint(0, 0xFFFFFF):06X}"
    elif user := await models.User.get_or_none(name=name):
        mention = "você" if name == ctx.author.name else f"@{name}"
        ctx.response = f"{mention} usa a cor {user.color}"
        if color_name := await color.ColorAPI.name(user.color[1:]):
            ctx.response += f" ({color_name})"
        if user.saved_color:
            ctx.response += f" e salvou a cor {user.saved_color}"
    else:
        ctx.response = f"@{name} ainda não foi registrado (não usou nenhum comando)"
