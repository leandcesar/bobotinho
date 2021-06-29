# -*- coding: utf-8 -*-
from bobotinho.cogs.commands.cookies import resetting_daily
from bobotinho.database import models
from bobotinho.utils import checks, convert

description = "Presenteie algum usuário com seu cookie"
aliases = ["give"]
usage = "digite o comando e o nome de alguém para presenteá-lo com seu cookie"
extra_checks = [checks.is_banword]


async def func(ctx, arg: str):
    if resetting_daily():
        ctx.response = "a fornada de cookies está sendo preparada, aguarde"
        return
    name = convert.str2username(arg)
    cookie_from, _ = await models.Cookie.get_or_create(id=ctx.author.id, name=ctx.author.name)
    if not name:
        ctx.response = "nome de usuário inválido"
    elif name == ctx.bot.nick:
        ctx.response = "eu não quero seu cookie"
    elif name == ctx.author.name:
        ctx.response = "você presenteou você mesmo, uau!"
    elif not (user := await models.User.get_or_none(name=name)):
        ctx.response = f"@{name} ainda não foi registrado (não usou nenhum comando)"
    elif not user.mention:
        ctx.response = "esse usuário optou por não permitir mencioná-lo"
    elif cookie_from.daily >= 1:
        cookie_to, _ = await models.Cookie.get_or_create(name=name)
        await cookie_from.donate()
        await cookie_to.receive()
        ctx.response = f"você presenteou @{name} com um cookie 🎁"
    else:
        ctx.response = "você já usou seu cookie diário, a próxima fornada sai às 6 da manhã! ⌛"
