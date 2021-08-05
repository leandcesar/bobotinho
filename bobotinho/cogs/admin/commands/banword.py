# -*- coding: utf-8 -*-
from bobotinho.database.models import Channel
from bobotinho.utils import convert, roles

aliases = ["bw"]
description = "Adicione ou remova um termo banido"
usage = 'digite o comando, "+" (para adicionar) ou "-" (para remover) e o termo'
extra_checks = [roles.mod]


async def command(ctx, arg1: str, arg2: str):
    if arg1 in ["-", "+"] and arg2:
        operator = arg1
        word = convert.str2ascii(arg2)
        if not all(x.isalnum() or x.isspace() for x in word):
            ctx.response = "o termo deve conter apenas letras, números e espaço"
        elif operator == "+" and word in ctx.bot.channels[ctx.channel.name]["banwords"]:
            ctx.response = "esse termo já é um termo banido"
        elif operator == "-" and word not in ctx.bot.channels[ctx.channel.name]["banwords"]:
            ctx.response = "esse termo não é um termo banido"
        elif operator == "+":
            ctx.bot.channels[ctx.channel.name]["banwords"].append(word)
            await Channel.append_json(
                ctx.bot.channels[ctx.channel.name]["id"], "banwords", word, ctx.author.id
            )
            ctx.response = "esse termo foi adicionado aos termos banidos"
        elif operator == "-":
            ctx.bot.channels[ctx.channel.name]["banwords"].remove(word)
            await Channel.remove_json(
                ctx.bot.channels[ctx.channel.name]["id"], "banwords", word
            )
            ctx.response = "esse termo foi removido dos termos banidos"
