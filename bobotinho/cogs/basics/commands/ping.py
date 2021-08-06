# -*- coding: utf-8 -*-
description = "Verifique se o bot está online"
aliases = ["pong"]


async def command(ctx):
    invoke_by = ctx.message.content.partition(" ")[0][len(ctx.prefix):].lower()
    ctx.response = "ping 🏓" if invoke_by == "pong" else "pong 🏓"
