# -*- coding: utf-8 -*-
from bobotinho.cogs.commands import pets as P
from bobotinho.database import models

description = "Devolva um pet em troca de parte da quantia que gastou"
usage = "digite o comando e o nome ou espécie do pet que quer devolver"


async def func(ctx, *, content: str):
    if pet := await models.Pet.find(id=ctx.author.id, name=content.title(), specie=content.lower()):
        price = round(P.all_pets[pet.specie].price * 0.7)
        emoji = P.all_pets[pet.specie].emoji
        cookie = await models.Cookie.get(id=ctx.author.id)
        cookie.stocked += price
        await cookie.save()
        await pet.delete()
        ctx.response = f"você devolveu {pet} {emoji} em troca de {price} cookies"
    else:
        ctx.response = f'adquira um pet em troca de cookies ("{ctx.prefix}petlist")'
