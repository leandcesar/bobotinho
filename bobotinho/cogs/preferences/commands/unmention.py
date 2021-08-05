# -*- coding: utf-8 -*-
from bobotinho.database.models import User

description = "Impeça que outros usuários utilizem comandos direcionados a você"


async def command(ctx):
    await User.filter(id=ctx.author.id).update(mention=False)
    ctx.response = "outros usuários não poderão mais mencionar você através dos comandos"
