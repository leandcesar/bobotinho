# -*- coding: utf-8 -*-
from bobotinho.database import User
from bobotinho.utils import convert

description = "Saiba o código hexadecimal da cor de algum usuário"
aliases = ["colour"]


async def command(ctx, arg: str = ""):
    name = convert.str2name(arg, default=ctx.author.name)
    if name == ctx.bot.nick:
        ctx.response = "eu uso a cor #FFFFFF (White)"
    elif not (user := await User.get_or_none(name=name)):
        ctx.response = f"@{name} ainda não foi registrado (não usou nenhum comando)"
    elif arg and not user.mention:
        ctx.response = "esse usuário optou por não permitir mencioná-lo"
    else:
        mention = "você" if name == ctx.author.name else f"@{name}"
        ctx.response = f"{mention} usa a cor {user.color}"
        try:
            color = await ctx.bot.api.color(user.color)
            color_name = color["name"]
            ctx.response += f" ({color_name})"
        except Exception:
            pass
        if user.saved_color:
            ctx.response += f" e salvou a cor {user.saved_color}"
