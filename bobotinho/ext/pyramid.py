# -*- coding: utf-8 -*-

__all__ = ("Pyramid",)


class Pyramid:
    def __init__(self):
        self.user = ""
        self.word = ""
        self.i = 0
        self.max = 0

    def __bool__(self) -> bool:
        return self.i <= 1 < self.max

    def __len__(self) -> int:
        return self.max

    def __add__(self, x: int):
        self.i += 1
        self.max += 1
        return self

    def __sub__(self, x: int):
        self.i -= 1
        return self

    def is_next(self, user: str, word: str, x: int) -> bool:
        if self.user != user or self.word != word:
            return False
        elif x < 0:
            return self.i - 1 == - x
        else:
            return self.i + 1 == x and len(self) < x

    def update(self, user: str, content: str) -> bool:
        parts = content.strip().split()
        word = parts[0]
        count = parts.count(word)
        if self.is_next(user, word, count):
            self += 1
        elif self.is_next(user, word, -count):
            self -= 1
        elif count == 1:
            self.user = user
            self.word = word
            self.i = self.max = 1
        else:
            self.user = self.word = ""
            self.i = self.max = 0
        return bool(self)
