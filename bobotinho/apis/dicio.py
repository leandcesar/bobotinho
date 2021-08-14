# -*- coding: utf-8 -*-
import html
import requests
from typing import Optional

from bobotinho import config
from bobotinho.utils import convert


class Dicio:
    base_url = config.dicio_url

    @classmethod
    def exists(cls, word: str) -> Optional[bool]:
        url = f"{cls.base_url}/{word}"
        try:
            response = requests.get(url)
            text = html.unescape(response.text)
        except Exception:
            return None
        start = text.find("<h1")
        if start != -1:
            start += len("<h1")
        start = text.find(">", start) + 1
        end = text.find("</h1>", start)
        title = text[start:end] if -1 < start < end else text
        return convert.str2ascii(title) == convert.str2ascii(word)
