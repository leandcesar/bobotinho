# -*- coding: utf-8 -*-
from bobotinho.cogs.commands import dungeons as D
from bobotinho.database import models
from bobotinho.utils import timetools

description = "Entre na dungeon e adquira experiência sem precisar tomar uma escolha"
aliases = ["fed", "fd"]


async def func(ctx):
    if dungeon := await models.Dungeon.get_or_none(user_id=ctx.author.name):
        if not dungeon.sub_class:
            option1, option2 = D.options_sub_class(dungeon.class_, dungeon.gender)
            ctx.response = (
                f'antes de continuar, digite "{ctx.prefix}ed" e sua nova classe: {option1} ou {option2}'
            )
        elif dungeon.updated_ago.total_seconds() > 10800:
            dungeon, response = D.resume_dungeon(dungeon)
            dungeon.last_at = ctx.message.timestamp
            await dungeon.save()
            ctx.response = response
        else:
            ctx.response = f"aguarde {timetools.clean(dungeon.updated_ago)} para entrar em outra dungeon ⌛"
    else:
        ctx.response = (
            "antes de continuar, escolha sua classe! "
            f'Digite "{ctx.prefix}ed" e: Guerreiro(a), Arqueiro(a) ou Mago(a)'
        )
