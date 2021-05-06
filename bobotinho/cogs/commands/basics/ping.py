# -*- coding: utf-8 -*-
description = "Verifique se o bot está online"
aliases = ["pong"]


async def func(ctx):
    ctx.response = "ping 🏓" if ctx.command.invocation == "pong" else "pong 🏓"
