# -*- coding: utf-8 -*-
from bobotinho.cogs.commands import dungeons as D
from bobotinho.database import models
from bobotinho.utils import timetools

description = "Entre na dungeon, faça sua escolha e adquira experiência"
aliases = ["ed"]


async def func(ctx, *, content: str = ""):
    choice = content.lower()
    if dungeon := await models.Dungeon.get_or_none(user_id=ctx.author.name):
        if not dungeon.sub_class:
            if sub_class := D.choose_sub_class(choice, dungeon.class_, dungeon.gender):
                dungeon.sub_class = sub_class
                c = D.classes[dungeon.class_][dungeon.gender][dungeon.sub_class][dungeon.level//10]
                await dungeon.save()
                ctx.response = f"agora você é {c}"
            else:
                option1, option2 = D.options_sub_class(dungeon.class_, dungeon.gender)
                ctx.response = f"antes de continuar, digite o comando e sua nova classe: {option1} ou {option2}"
        elif dungeon.i:
            if choice in ["1", "2"]:
                dungeon, response = D.resume_dungeon(dungeon, choice)
                await dungeon.save()
                ctx.response = response
            else:
                ctx.response = D.generate_dungeon(dungeon.i)[0]["quote"]
        elif dungeon.updated_ago.total_seconds() > 10800:
            d, dungeon.i = D.generate_dungeon()
            await dungeon.save()
            ctx.response = d["quote"]
        else:
            ctx.response = f"aguarde {timetools.clean(dungeon.updated_ago)} para entrar em outra dungeon ⌛"
    elif c := D.choose_class(choice):
        dungeon = await models.Dungeon.create(
            user_id=ctx.author.name,
            class_=c["class_"],
            gender=c["gender"],
            i=D.generate_dungeon()[1],
        )
        emoji = D.classes[dungeon.class_]["emoji"]
        ctx.response = f"você escolheu {choice.title()}! {emoji}"
    else:
        ctx.response = (
            "antes de continuar, escolha sua classe! "
            "Digite o comando e: Guerreiro(a), Arqueiro(a) ou Mago(a)"
        )
