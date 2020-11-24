# -*- coding: utf-8 -*-

"""
bobotinho - Twitch bot for Brazilian offstream chat entertainment
Copyright (C) 2020  Leandro César

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import re
import traceback as tb

from functools import wraps
from typing import Union
from twitchio.dataclasses import Context, Message
from utils import time


def case_insensitive(prefix: str = "%"):
    def decorator(func):
        @wraps(func)
        async def inner(bot, message):
            if message.content.startswith(prefix) and len(message.content) > 1:
                content = message.content.replace("󠀀", "")  # removes invisible character
                if content[1] == " ":
                    content = content.replace(" ", "", 1)
                try:
                    command, residue = content.split(maxsplit=1)
                    content = command.lower() + " " + residue
                except:
                    content = content.lower()
                message.content = content

            return await func(bot, message)

        return inner

    return decorator


def command(target: str):
    command = re.match(r"%?([0-9A-Za-z]+|%)$", target)
    if not command:
        return ""
    return command.group(1).lower()


def cooldown(target, delay, now=None):
    target = time.parse_date(target)
    now = time.parse_date(now) if now else time.datetime.datetime.utcnow()
    if target > now:
        # what...?
        return None
    delay = time.parse_delta(delay)
    delta = now - target
    if delta > delay:
        return False
    return time.date_format(delay - delta)


def date(target):
    return time.parse_date(target)


def number(target: Union[int, float]):
    if float(target) > 1e15:
        raise ValueError(f"Expected `float(target)` <= 1e15, not `{target}`")
    elif isinstance(target, int):
        return f"{target:,d}".replace(",", ".")
    elif isinstance(target, float):
        return f"{target:,.2f}"[::-1].replace(",", ".").replace(".", ",", 1)[::-1]


def timesince(target, now=None, future_target: bool = False):
    target = time.parse_date(target)
    now = time.parse_date(now) if now else time.datetime.datetime.utcnow()
    delta, future = (target - now, True) if target > now else (now - target, False)
    if future_target != future:
        return False
    return time.date_format(delta)


def traceback(err):
    format_tb = "".join(tb.format_tb(err.__traceback__))
    return f"{format_tb}{type(err).__name__}: {err}"


def user(target: str):
    if target.startswith("@"):
        target = target[1:]
    if target.endswith(","):
        target = target[:-1]
    return target.lower()
