# -*- coding: utf-8 -*-
from bobotinho.cogs.commands import pets as P
from bobotinho.database import models
from bobotinho.utils import checks

description = "Dê um nome para o seu pet"
usage = "digite o comando e o nome que desejar para seu pet"
extra_checks = [checks.is_banword]


async def func(ctx, *, content: str):
    pets = await models.Pet.filter(user_id=ctx.author.id).all()
    if len(pets) > 1 and " " in content:
        specie, name = content.split(maxsplit=1)
        specie = specie.lower()
        name = name.title()
    elif len(pets) == 1:
        specie = pets[0].specie
        name = content.title()
    if len(pets) == 0:
        ctx.response = f'adquira um pet em troca de cookies ("{ctx.prefix}petlist")'
    elif len(pets) > 1 and (" " not in content or not any([specie == pet.specie for pet in pets])):
        ctx.response = "você tem mais de um pet, então especifque a espécie e depois o nome"
    elif len(name) > 32:
        ctx.response = "esse nome é muito comprido para seu pet"
    elif not all(char.isalpha() or char.isspace() for char in name):
        ctx.response = "esse nome não é válido (apenas letras e espaços)"
    else:
        # TODO: se o cara tiver 2 pets da mesma especie, vai dar ruim
        await models.Pet.filter(user_id=ctx.author.id, specie=specie).update(name=name)
        ctx.response = f"agora seu pet se chama {name} {P.all_pets[specie].emoji}"
