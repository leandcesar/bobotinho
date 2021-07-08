# -*- coding: utf-8 -*-
from bobotinho.database import models

description = "Impeça que outros usuários utilizem comandos direcionados a você"


async def func(ctx):
    await models.User.filter(id=ctx.author.id).update(mention=False)
    ctx.response = "outros usuários não poderão mais mencionar você através dos comandos"
