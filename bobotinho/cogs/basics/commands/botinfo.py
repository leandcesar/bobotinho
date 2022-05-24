# -*- coding: utf-8 -*-
from bobotinho.database import Channel

description = "Veja as principais informações sobre o bot"
aliases = ["bot", "info"]


async def command(ctx):
    num_channels = await Channel.all().count()
    num_instances = (num_channels // 50) + 1
    num_commands = len(ctx.bot.commands)
    ctx.response = (
        f"estou conectado à {num_channels} canais, com {num_commands} comandos, "
        f"rodando em {num_instances} instâncias, feito por @{ctx.bot.dev}"
    )
