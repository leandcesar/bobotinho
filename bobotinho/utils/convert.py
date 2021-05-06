# -*- coding: utf-8 -*-
import random
import re
from typing import Union, Optional
from unidecode import unidecode


def str2ascii(target: str) -> str:
    return unidecode(target).lower().strip()


def txt2randomline(target: str) -> str:
    with open(target, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    return random.choice(lines)


def number2str(target: Union[int, float]) -> Optional[str]:
    if isinstance(target, int):
        return f"{target:,d}".replace(",", ".")
    if isinstance(target, float):
        return f"{target:,.2f}"[::-1].replace(",", ".").replace(".", ",", 1)[::-1]


def str2float(target: Optional[str]) -> Optional[float]:
    try:
        return float(target.replace(",", "."))
    except Exception:
        return None


def str2int(target: Optional[str]) -> Optional[int]:
    try:
        return int(target)
    except Exception:
        return None


def str2hexcode(target: Optional[str]) -> Optional[str]:
    if target:
        return re.match(r"#(?:[0-9A-Fa-f]{6})$", target).group(0)


def str2username(target: Optional[str]) -> Optional[str]:
    if not target:
        return None
    if target[0] == "@":
        target = target[1:]
    if target[-1] == ",":
        target = target[:-1]
    if target.replace("_", "").isalnum():
        return target.lower()
