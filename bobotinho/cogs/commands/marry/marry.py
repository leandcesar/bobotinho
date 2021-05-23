# -*- coding: utf-8 -*-
import time

from bobotinho.database import models
from bobotinho.utils import checks, convert

description = "Case-se e seja feliz para sempre, mas isso custará cookies"
usage = "digite o comando e o nome de quem você quer pedir em casamento"
extra_checks = [checks.is_banword]


async def func(ctx, arg: str):
    ctx.bot.cache["weddings"] = {
        k: v
        for k, v in ctx.bot.cache.get("weddings", {}).items()
        if v["time"] < time.monotonic()
    }
    name = convert.str2username(arg)
    if not name:
        ctx.response = "nome de usuário inválido"
    elif name == ctx.bot.nick:
        ctx.response = "não fui programado para fazer parte de um relacionamento"
    elif name == ctx.author.name:
        ctx.response = "você não pode se casar com você mesmo..."
    elif ctx.author.name in ctx.bot.cache["weddings"].keys():
        ctx.response = (
            "antes você precisa responder ao pedido que lhe fizeram! "
            f'Digite "{ctx.prefix}yes" ou "{ctx.prefix}no"'
        )
    elif any([v for v in ctx.bot.cache["weddings"].values() if ctx.author.name == v["name"]]):
        ctx.response = "vá com calma garanhão, você acabou de pedir alguém em casamento"
    elif name in ctx.bot.cache["weddings"].keys():
        ctx.response = f"alguém chegou primeiro e já fez uma proposta à mão de @{name}"
    elif any([v for v in ctx.bot.cache["weddings"].values() if name == v["name"]]):
        ctx.response = f"@{name} está aguardando a resposta de outra pessoa"
    elif (
        await models.Wedding.exists(user_1_id=ctx.author.name)
        or await models.Wedding.exists(user_2_id=ctx.author.name)
    ):
        ctx.response = "traição é inaceitável, ao menos se divorcie antes de partir pra outra"
    elif (
        await models.Wedding.exists(user_1_id=name)
        or await models.Wedding.exists(user_2_id=name)
    ):
        ctx.response = f"controle seu desejo por pessoas casadas, @{name} já está em um compromisso"
    elif (cookie := await models.Cookie.get_or_none(name=ctx.author.name)) and cookie.stocked >= 100:
        ctx.bot.cache["weddings"][name] = {"name": ctx.author.name, "time": time.monotonic() + 60}
        ctx.response = (
            f"você pediu a mão de @{name}, o usuário deve "
            f'digitar "{ctx.prefix}yes" ou "{ctx.prefix}no" 💐💍'
        )
    else:
        ctx.response = "para pagar a aliança e todo o casório, você deve ter 100 cookies estocados"
