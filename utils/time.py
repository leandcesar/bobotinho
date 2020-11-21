# -*- coding: utf-8 -*-

import datetime

from dateutil.relativedelta import relativedelta
from typing import Union
from twitchio.dataclasses import Context, Message


def parse_date(target):
    if not target:
        raise ValueError(f"Not expected `{target}` value")
    elif isinstance(target, Context):
        return target.message.timestamp
    elif isinstance(target, Message):
        return target.timestamp
    elif isinstance(target, datetime.datetime):
        return target
    elif isinstance(target, datetime.date):
        d = target
        t = datetime.time(0, 0, 0)
        return datetime.datetime(d.year, d.month, d.day, t.hour, t.minute, t.second)
    elif isinstance(target, relativedelta):
        return datetime.datetime.utcnow() + target
    elif isinstance(target, datetime.time):
        d = datetime.date.today()
        t = target
        return datetime.datetime(d.year, d.month, d.day, t.hour, t.minute, t.second)
    elif isinstance(target, (int, float)):
        return datetime.datetime.fromtimestamp(target)
    else:
        raise TypeError(f"Not expected `{type(target).__name__}` type")


def parse_delta(target: Union[int, datetime.timedelta]):
    if not target:
        raise ValueError(f"Not expected `{target}` value")
    elif isinstance(target, int):
        return datetime.timedelta(seconds=target)
    elif isinstance(target, datetime.timedelta):
        return target
    else:
        raise TypeError(f"Not expected `{type(target).__name__}` type")


def plural(x: str, i: int):
    if x == "mês":
        return x if abs(i) == 1 else "meses"
    return x if abs(i) == 1 else x + "s"


def date_format(delta: datetime.timedelta):
    y, d = divmod(delta.days, 365)
    M, d = divmod(d, 30)
    m, s = divmod(delta.seconds, 60)
    H, m = divmod(m, 60)

    response = ""
    if y:
        response += f'{y} {plural("ano", y)}'
    if M:
        response += f' {M} {plural("mês", M)}'
    if d:
        response += f' {d} {plural("dia", d)}'
    response += f" {H:02d}:{m:02d}:{s:02d}"
    
    if not response:
        raise Exception("Not expected `None` value")
    return response.strip()
