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
    elif not (
        await models.Wedding.exists(user_1_id=ctx.author.id, divorced=False)
        or await models.Wedding.exists(user_2_id=ctx.author.id, divorced=False)
    ):
        ctx.response = "você não está casado com ninguém"
    elif not (user := await models.User.get_or_none(name=name)):
        ctx.response = f"@{name} ainda não foi registrado (não usou nenhum comando)"
    elif wedding := (
        await models.Wedding.get_or_none(user_1_id=ctx.author.id, user_2_id=user.id, divorced=False)
        or await models.Wedding.get_or_none(user_1_id=user.id, user_2_id=ctx.author.id, divorced=False)
    ):
        wedding.divorced = True
        await wedding.save()
        ctx.response = (
            "então, é isso... da próxima vez, case-se com alguém "
            "que realmente te ame, e não qualquer pessoa por aí"
        )
    else:
        ctx.response = "você não sabe nem o nome da pessoa com quem está casado?"
