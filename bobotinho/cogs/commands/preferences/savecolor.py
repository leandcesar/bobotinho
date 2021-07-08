# -*- coding: utf-8 -*-
from bobotinho.database import models
from bobotinho.utils import convert

description = "Salve um código hexadecimal de cor"


async def func(ctx, arg: str = ""):
    if color := convert.str2hexcode(arg or ctx.author.colour):
        await models.User.filter(id=ctx.author.id).update(saved_color=color)
        ctx.response = (
            f'você salvou a cor {color.upper()} e pode visualizá-la usando "{ctx.prefix}color"'
        )
    else:
        ctx.response = "esse não é um código hexadecimal de cor válido"
