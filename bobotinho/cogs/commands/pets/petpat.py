# -*- coding: utf-8 -*-
from bobotinho.cogs.commands import pets as P
from bobotinho.database import models

description = "Faça carinho no seu pet"


async def func(ctx):
    if all_pets := await models.Pet.filter(user_id=ctx.author.id).all():
        pets = P.join_pets(all_pets, formatter="{pet} {emoji}")
        ctx.response = f"você fez carinho em {pets}"
    else:
        ctx.response = f'adquira um pet em troca de cookies ("{ctx.prefix}petlist")'
