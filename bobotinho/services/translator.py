# -*- coding: utf-8 -*-
from deep_translator import GoogleTranslator

__all__ = ("Translator",)


class Translator:
    def translate(self, *, text: str, source: str = "auto", target: str = "pt") -> str:
        return GoogleTranslator(source=source, target=target).translate(text)

    async def close(self) -> None:
        pass
