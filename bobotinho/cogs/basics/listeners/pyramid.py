# -*- coding: utf-8 -*-
from typing import Optional


class Pyramid:
    def __init__(self):
        self.init()

    def init(self, user: Optional[str] = None, word: Optional[str] = None, count: int = 0) -> None:
        self.user = user
        self.word = word
        self.i = self.max = count
        self.raising = True

    def increase(self) -> None:
        self.i += 1
        self.max += 1

    def decrease(self) -> Optional[str]:
        self.i -= 1
        self.raising = False
        if self.i <= 1 and self.max >= 3:
            return f"você fez uma pirâmide de {self.max} {self.word}"

    def update(self, ctx) -> Optional[str]:
        parts = ctx.message.content.strip().split()
        word = parts[0]
        count = parts.count(word)
        same = (self.user == ctx.author.name and self.word == word)
        if len(parts) != count:
            return self.init()
        if same and self.raising and self.i + 1 == count:
            return self.increase()
        if same and self.i - 1 == count:
            return self.decrease()
        if count == 1:
            return self.init(ctx.author.name, word, 1)
        return self.init()


async def listener(ctx) -> None:
    if not ctx.bot.channels[ctx.channel.name].get("pyramid"):
        ctx.bot.channels[ctx.channel.name]["pyramid"] = Pyramid()
    ctx.response = ctx.bot.channels[ctx.channel.name]["pyramid"].update(ctx)
