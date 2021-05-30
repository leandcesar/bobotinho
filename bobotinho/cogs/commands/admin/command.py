# -*- coding: utf-8 -*-
from bobotinho.database import models
from bobotinho.utils import checks, convert

aliases = ["cmd"]
description = "Ative ou desative um comando"
usage = 'digite o comando, "+" (para ativar) ou "-" (para desativar) e o nome de um comando'
extra_checks = [checks.is_mod]


async def func(ctx, arg1: str, arg2: str):
    if (operator := arg1) not in ["-", "+"]:
        return
    command = None
    if name := convert.str2ascii(arg2):
        for c in ctx.bot.commands.values():
            if name == c.name or (c.aliases and name in c.aliases):
                command = c
                break
    if not command:
        ctx.response = "esse comando não existe"
    elif command.name == "command":
        ctx.response = f'"{command.name}" não pode ser desativado'
    elif operator == "+" and command.name not in ctx.bot.channels[ctx.channel.name]["disabled"]:
        ctx.response = f'"{command.name}" já está ativado'
    elif operator == "-" and command.name in ctx.bot.channels[ctx.channel.name]["disabled"]:
        ctx.response = f'"{command.name}" já está desativado'
    elif operator == "+":
        ctx.bot.channels[ctx.channel.name]["disabled"].remove(command.name)
        await models.Channel.remove_json(
            ctx.bot.channels[ctx.channel.name]["id"], "disabled", command.name
        )
        ctx.response = f'"{command.name}" foi ativado'
    elif operator == "-":
        ctx.bot.channels[ctx.channel.name]["disabled"].append(command.name)
        await models.Channel.append_json(
            ctx.bot.channels[ctx.channel.name]["id"], "disabled", command.name, ctx.author.id
        )
        ctx.response = f'"{command.name}" foi desativado'
