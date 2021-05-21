# -*- coding: utf-8 -*-
from bobotinho.database import models
from bobotinho.utils import convert

description = "Divorcie-se da pessoa com quem você é casada"
usage = "digite o comando e o nome da pessoa com quem se casou para se divorciar"


async def func(ctx, arg: str):
    name = convert.str2username(arg)
    if not name:
        ctx.response = "nome de usuário inválido"
    elif name == ctx.bot.nick:
        ctx.response = "eu nunca estaria casado com você"
    elif name == ctx.author.name:
        ctx.response = "você não pode se livrar de você mesmo"
    elif (
        await models.Wedding.exists(user_1_id=ctx.author.name)
        or await models.Wedding.exists(user_2_id=ctx.author.name)
    ):
        ctx.response = "você não está casado com ninguém"
    elif wedding := (
        await models.Wedding.get_or_none(user_1_id=ctx.author.name, user_2_id=name)
        or await models.Wedding.get_or_none(user_1_id=name, user_2_id=ctx.author.name)
    ):
        # TODO: alterar wedding.divorced = True em vez de deletar
        await wedding.delete()
        ctx.response = (
            "então, é isso... da próxima vez, case-se com alguém "
            "que realmente te ame, e não qualquer pessoa por aí"
        )
    else:
        ctx.response = "você não sabe nem o nome da pessoa com quem está casado?"
