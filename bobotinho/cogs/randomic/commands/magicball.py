# -*- coding: utf-8 -*-
from bobotinho.utils import convert

aliases = ["8ball"]
description = "Tenha sua pergunta respondida por uma previsão"
usage = "digite o comando e uma pergunta para receber uma previsão"


async def command(ctx, *, content: str):
    predict = convert.list2randomline(
        [
            "ao meu ver, sim",
            "com certeza",
            "com certeza não",
            "concentre-se e pergunte novamente",
            "decididamente sim",
            "definitivamente sim",
            "dificilmente",
            "é complicado...",
            "é melhor você não saber",
            "fontes dizem que não",
            "impossível isso acontecer",
            "impossível prever isso",
            "jamais",
            "muito duvidoso",
            "nunca",
            "não",
            "não conte com isso",
            "não é possível prever isso",
            "pergunta nebulosa, tente novamente",
            "pergunte novamente mais tarde...",
            "pode apostar que sim",
            "possivelmente",
            "provavelmente...",
            "sem dúvidas",
            "sim",
            "sinais apontam que sim",
            "talvez",
            "você ainda tem dúvidas?",
            "você não acreditaria...",
        ]
    )
    ctx.response = f"{predict} 🎱"
