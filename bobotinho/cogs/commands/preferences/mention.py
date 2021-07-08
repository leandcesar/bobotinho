# -*- coding: utf-8 -*-
from bobotinho.database import models

description = "Permita que outros usuários utilizem comandos direcionados a você"


async def func(ctx):
    await models.User.filter(id=ctx.author.id).update(mention=True)
    ctx.response = "agora outros usuários poderão mencionar você através dos comandos"
