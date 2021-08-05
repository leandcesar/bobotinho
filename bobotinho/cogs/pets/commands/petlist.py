# -*- coding: utf-8 -*-
from bobotinho.cogs.pets import join_pets, random_pets

description = "Veja os pets disponíveis para adquirir"


async def command(ctx):
    pet_list = list(sorted(random_pets().values(), key=lambda k: k[2]))
    pets = join_pets(pet_list, formatter="{pet} ({price})", sep=", ")
    ctx.response = f"pets disponíveis hoje: {pets}"
