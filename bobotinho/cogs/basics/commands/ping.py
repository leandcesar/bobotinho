# -*- coding: utf-8 -*-
description = "Verifique se o bot está online"
aliases = ["pong"]


async def command(ctx):
    ctx.response = f"ping 🏓 (instância {ctx.bot.instance})"
