# -*- coding: utf-8 -*-
from bobotinho.utils import convert

description = "Dê um beijinho em alguém do chat"
usage = "digite o comando e o nome de alguém para beijá-lo"


async def command(ctx, arg: str):
    name = convert.str2name(arg)
    if name == ctx.bot.nick:
        ctx.response = "😳"
    elif name == ctx.author.name:
        ctx.response = "você tentou se beijar... FeelsBadMan"
    else:
        ctx.response = f"você deu um beijinho em @{name} 😚"
