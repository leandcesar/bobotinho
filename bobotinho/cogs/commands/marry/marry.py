# -*- coding: utf-8 -*-
from bobotinho.database import models
from bobotinho.utils import checks, convert

description = "Case-se e seja feliz para sempre, mas isso custará cookies"
usage = "digite o comando e o nome de quem você quer pedir em casamento"
extra_checks = [checks.banword]


async def func(ctx, arg: str):
    name = convert.str2username(arg)
    if not name:
        ctx.response = "nome de usuário inválido"
    elif name == ctx.bot.nick:
        ctx.response = "não fui programado para fazer parte de um relacionamento"
    elif name == ctx.author.name:
        ctx.response = "você não pode se casar com você mesmo..."
    elif someone := ctx.bot.cache.get(f"marry-{ctx.author.name}"):
        ctx.response = (
            f"antes você precisa responder ao pedido de @{someone}! "
            f'Digite "{ctx.prefix}yes" ou "{ctx.prefix}no"'
        )
    elif someone := ctx.bot.cache.get(f"marry-{name}"):
        ctx.response = f"@{someone} chegou primeiro e já fez uma proposta à mão de @{name}"
    elif (
        await models.Wedding.exists(user_1_id=ctx.author.id, divorced=False)
        or await models.Wedding.exists(user_2_id=ctx.author.id, divorced=False)
    ):
        ctx.response = "traição é inaceitável, ao menos se divorcie antes de partir pra outra"
    elif not (user := await models.User.get_or_none(name=name)):
        ctx.response = f"@{name} ainda não foi registrado (não usou nenhum comando)"
    elif not user.mention:
        ctx.response = "esse usuário optou por não permitir mencioná-lo"
    elif (
        await models.Wedding.exists(user_1_id=user.id, divorced=False)
        or await models.Wedding.exists(user_2_id=user.id, divorced=False)
    ):
        ctx.response = f"controle seu desejo por pessoas casadas, @{name} já está em um compromisso"
    elif (cookie := await models.Cookie.get_or_none(name=ctx.author.name)) and cookie.stocked >= 100:
        ctx.bot.cache.set(f"marry-{name}", ctx.author.name, ex=180)
        ctx.response = (
            f"você pediu a mão de @{name}, o usuário deve "
            f'digitar "{ctx.prefix}yes" ou "{ctx.prefix}no" 💐💍'
        )
    else:
        ctx.response = "para pagar a aliança e todo o casório, você deve ter 100 cookies estocados"
