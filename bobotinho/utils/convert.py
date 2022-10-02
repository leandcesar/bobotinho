# -*- coding: utf-8 -*-
import json
import string

letters_and_digits = string.ascii_letters + string.digits


def str2hex(value: str) -> str:
    return "".join(x for x in value if x in letters_and_digits).encode().hex()


def str2int(value: str) -> int:
    return int(str2hex(value), base=16)


def json2dict(filename: str) -> dict:
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)
