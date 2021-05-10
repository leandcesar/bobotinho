# -*- coding: utf-8 -*-
from bobotinho.cogs.commands import pets as P
from bobotinho.database import models

description = "Adquira um dos pets disponíveis na loja"
usage = "digite o comando e um dos pets disponíveis na loja para adquirí-lo"


async def func(ctx, arg: str):
    if pet := P.random_pets().get(arg.lower()):
        if cookie := await models.Cookie.get_or_none(user_id=ctx.author.name):
            if await models.Pet.filter(user_id=ctx.author.id).count() >= 3:
                ctx.response = "você já possui a quantidade máxima de pets"
            elif cookie.stocked < pet.price:
                ctx.response = f"estoque {pet.price} cookies para adquirir {pet.specie} {pet.emoji}"
            else:
                await models.Pet.create(user_id=ctx.author.name, specie=pet.specie)
                await cookie.stock(-pet.price)
                ctx.response = f"você adquiriu {pet.specie} {pet.emoji}, agora escolha o nome!"
        else:
            ctx.response = f"comece a estocar cookies para adquirir um pet ({ctx.prefix}stock)"
    else:
        ctx.response = f"escolha um dos pets disponíveis na lista de hoje ({ctx.prefix}petlist)"
