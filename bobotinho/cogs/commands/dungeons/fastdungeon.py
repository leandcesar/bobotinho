# -*- coding: utf-8 -*-
from bobotinho.cogs.commands import dungeons as D
from bobotinho.database import models
from bobotinho.utils import timetools

description = "Entre na dungeon e adquira experiência sem precisar tomar uma escolha"
aliases = ["fed", "fd"]


async def func(ctx):
    if player := await models.Player.get_or_none(name=ctx.author.name):
        if not player.sub_class:
            option1, option2 = D.options_sub_class(player.class_, player.gender)
            ctx.response = (
                f'antes de continuar, digite "{ctx.prefix}ed" e sua nova classe: {option1} ou {option2}'
            )
        elif cooldown := timetools.on_cooldown(player.updated_at, now=ctx.message.timestamp, s=10800):
            ctx.response = f"aguarde {cooldown} para entrar em outra dungeon ⌛"
        else:
            multiplier = 2 if ctx.user.sponsor else 1
            player, response = D.resume_dungeon(player, multiplier=multiplier)
            player.last_at = ctx.message.timestamp
            await player.save()
            ctx.response = response
    else:
        ctx.response = (
            "antes de continuar, escolha sua classe! "
            f'Digite "{ctx.prefix}ed" e: Guerreiro(a), Arqueiro(a) ou Mago(a)'
        )