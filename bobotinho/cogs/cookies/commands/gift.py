# -*- coding: utf-8 -*-
from bobotinho.cogs.cookies import resetting_daily
from bobotinho.database.models import Cookie, User
from bobotinho.utils import convert

description = "Presenteie algum usuário com seu cookie"
aliases = ["give"]
usage = "digite o comando e o nome de alguém para presenteá-lo com seu cookie"


async def command(ctx, arg: str):
    if resetting_daily():
        ctx.response = "a fornada de cookies está sendo preparada, aguarde"
        return
    name = convert.str2name(arg)
    cookie_from, _ = await Cookie.get_or_create(id=ctx.author.id, name=ctx.author.name)
    if name == ctx.bot.nick:
        ctx.response = "eu não quero seu cookie"
    elif name == ctx.author.name:
        ctx.response = "você presenteou você mesmo, uau!"
    elif not (user := await User.get_or_none(name=name)):
        ctx.response = f"@{name} ainda não foi registrado (não usou nenhum comando)"
    elif not user.mention:
        ctx.response = "esse usuário optou por não permitir mencioná-lo"
    elif cookie_from.daily >= 1:
        cookie_to, _ = await Cookie.get_or_create(name=name)
        await cookie_from.donate()
        await cookie_to.receive()
        ctx.response = f"você presenteou @{name} com um cookie 🎁"
    else:
        ctx.response = "você já usou seu cookie diário, a próxima fornada sai às 6 da manhã! ⌛"
