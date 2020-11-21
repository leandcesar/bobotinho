# -*- coding: utf-8 -*-


class Pyramid:
    def __init__(self):
        self.init()

    def init(self, user: str = None, word: str = None, count: int = 0):
        self.user = user
        self.word = word
        self.i = self.max = count
        self.raising = True
        self.complete = False

    def increase(self):
        self.i += 1
        self.max += 1

    def decrease(self):
        self.i -= 1
        self.raising = False
        if self.i == 1:
            self.complete = True

    async def update(self, message):
        parts = message.content.strip().split()
        word = parts[0]
        count = parts.count(word)
        same = self.user == message.author.name and self.word == word

        if len(parts) != count:
            self.init()
        elif same and self.raising and self.i + 1 == count:
            self.increase()
        elif same and self.i - 1 == count:
            self.decrease()
        elif count == 1:
            self.init(message.author.name, word, 1)
        else:
            self.init()

        if self.complete and self.max >= 3:
            response = f"@{self.user} fez uma pirâmide de {self.max} {self.word}"
            await message.channel.send(response)
            return True
