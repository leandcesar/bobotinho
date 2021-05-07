# -*- coding: utf-8 -*-
from typing import Optional

from bobotinho.logger import log


class Pyramid:
    def __init__(self):
        self.init()

    def init(self, user: str = None, word: str = None, count: int = 0) -> None:
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
            return f"@{self.user} fez uma pirâmide de {self.max} {self.word}"

    def update(self, message) -> Optional[str]:
        parts = message.content.strip().split()
        word = parts[0]
        count = parts.count(word)
        print(word)
        print(count)
        same = (self.user == message.author.name and self.word == word)
        if len(parts) != count:
            return self.init()
        if same and self.raising and self.i + 1 == count:
            return self.increase()
        if same and self.i - 1 == count:
            return self.decrease()
        if count == 1:
            return self.init(message.author.name, word, 1)
        return self.init()


async def event_message(bot, message) -> bool:
    if not bot.channels[message.channel.name].get("pyramid"):
        bot.channels[message.channel.name]["pyramid"] = Pyramid()
    response = bot.channels[message.channel.name]["pyramid"].update(message)
    if response:
        await message.channel.send(response)
        log.info(f"#{message.channel.name} @{bot.nick}: {response}")
        return True
