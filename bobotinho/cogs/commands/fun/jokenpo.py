# -*- coding: utf-8 -*-
import random

description = "Tente vencer no pedra, papel e tesoura"
aliases = ["jokempo"]
usage = 'digite o comando e "✊", "✋" ou "✌"'


async def func(ctx, arg: str):
    arg = (
        "✊"
        if arg == "pedra"
        else "✋"
        if arg == "papel"
        else "✌"
        if arg == "tesoura"
        else arg
    )
    emoji = random.choice(["✊", "✋", "✌"])
    if arg == emoji:
        ctx.response = f"eu escolhi {emoji} também, nós empatamos..."
    elif (arg, emoji) in [("✊", "✋"), ("✋", "✌"), ("✌", "✊")]:
        ctx.response = f"eu escolhi {emoji} e consegui te prever facilmente"
    elif (emoji, arg) in [("✊", "✋"), ("✋", "✌"), ("✌", "✊")]:
        ctx.response = f"eu escolhi {emoji}, você deu sorte dessa vez"
