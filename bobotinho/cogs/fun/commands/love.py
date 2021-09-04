# -*- coding: utf-8 -*-
import random
import re

description = "Veja quanto de amor existe entre você e alguém ou algo"
usage = "digite o comando e o nome de alguém ou algo para ver quanto há de amor"


async def command(ctx, *, content: str):
    emojis = ["😭", "😥", "💔", "😢", "😐", "😊", "❤", "💕", "💘", "😍", "PogChamp ❤"]
    percentage = random.randint(0, 100)
    emoji = emojis[round(percentage / 10)]
    if re.match(r"([\w\s]+\s&\s[\w\s]+)+$", content):  # Foo & bar
        ctx.response = f"entre {content}: {percentage}% de amor {emoji}"
    else:
        ctx.response = f"você & {content}: {percentage}% de amor {emoji}"
