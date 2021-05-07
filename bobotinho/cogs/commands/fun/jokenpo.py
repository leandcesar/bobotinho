# -*- coding: utf-8 -*-
import random

description = "Tente vencer no pedra, papel e tesoura"
aliases = ["jokempo"]
usage = 'digite o comando e "✊", "✋" ou "✌"'


async def func(ctx, arg1: str):
    emoji = random.choice("✊✋✌")
    if arg1 == emoji:
        ctx.response = f"eu escolhi {emoji} também, nós empatamos..."
    elif (arg1, emoji) in [("✊", "✋"), ("✋", "✌"), ("✌", "✊")]:
        ctx.response = f"eu escolhi {emoji} e consegui te prever facilmente"
    elif (emoji, arg1) in [("✊", "✋"), ("✋", "✌"), ("✌", "✊")]:
        ctx.response = f"eu escolhi {emoji}, você deu sorte dessa vez"
