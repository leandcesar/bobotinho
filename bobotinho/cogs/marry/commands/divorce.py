# -*- coding: utf-8 -*-
from bobotinho.database.models import User, Wedding
from bobotinho.utils import convert

description = "Divorcie-se da pessoa com quem você é casada"
usage = "digite o comando e o nome da pessoa com quem se casou para se divorciar"


async def command(ctx, arg: str):
    name = convert.str2name(arg)
    if name == ctx.bot.nick:
        ctx.response = "eu nunca estaria casado com você"
    elif name == ctx.author.name:
        ctx.response = "você não pode se livrar de você mesmo"
    elif not await Wedding.find(ctx.author.id):
        ctx.response = "você não está casado com ninguém"
    elif not (user := await User.get_or_none(name=name)):
        ctx.response = f"@{name} ainda não foi registrado (não usou nenhum comando)"
    elif wedding := await Wedding.find(ctx.author.id, user.id):
        await wedding.divorce()
        ctx.response = (
            "então, é isso... da próxima vez, case-se com alguém "
            "que realmente te ame, e não qualquer pessoa por aí"
        )
    else:
        ctx.response = "você não sabe nem o nome da pessoa com quem está casado?"
