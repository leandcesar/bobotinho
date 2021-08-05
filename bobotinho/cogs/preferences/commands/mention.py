# -*- coding: utf-8 -*-
from bobotinho.database.models import User

description = "Permita que outros usuários utilizem comandos direcionados a você"


async def command(ctx):
    await User.filter(id=ctx.author.id).update(mention=True)
    ctx.response = "agora outros usuários poderão mencionar você através dos comandos"
