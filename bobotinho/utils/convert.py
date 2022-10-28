# -*- coding: utf-8 -*-
import json
from string import ascii_letters
from string import digits
from typing import Union

__all__ = ("str_to_ascii", "str_to_hex", "str_to_int", "json_to_dict")

letters_and_digits = ascii_letters + digits


def str_to_ascii(value: str) -> str:
    reference = [('a', 'áàâãä'), ('e', 'éèêë'), ('i', 'íìîï'), ('o', 'óòôõö'), ('u', 'úùûü'), ('c', 'ç')]
    text = ""
    for char in value:
        for clear_vowal, possible_accents in reference:
            if char in possible_accents:
                text += clear_vowal
                break
        else:
            text += char
    return text


def str_to_hex(value: str) -> str:
    return "".join(x for x in value if x in letters_and_digits).encode().hex()


def str_to_int(value: str) -> int:
    return int(str_to_hex(value), base=16)


def json_to_dict(filename: str) -> Union[dict, list]:
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)
