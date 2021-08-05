# -*- coding: utf-8 -*-
from bobotinho.database.models import User

description = "Salve sua cidade para agilizar a previsão do tempo"
usage = "digite o comando e o nome da sua cidade para agilizar a previsão do tempo"


async def command(ctx, *, content: str):
    if len(content) <= 100:
        if content.lower() == "salvador":
            city = "Salvador, BR"
        city = content.title()
        await User.filter(id=ctx.author.id).update(city=city)
        ctx.response = (
            f'você salvou {city} como sua cidade, agora basta usar "{ctx.prefix}weather"'
        )
    else:
        ctx.response = "esse não é uma cidade válida"
