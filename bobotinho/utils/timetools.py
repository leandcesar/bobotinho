# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta, timezone
from typing import Union, Optional

pattern_relative_time = re.compile(
    r"""
    (?:in|daqui)\s
    (\b(?P<years>\d+)\s?(?:anos|ano|a)\b\s?)?
    (\b(?P<months>\d+)\s?(?:meses|mês|mes)\b\s?)?
    (\b(?P<weeks>\d+)\s?(?:semanas|semana)\b\s?)?
    (\b(?P<days>\d+)\s?(?:dias|dia|d)\b\s?)?
    (\b(?P<hours>\d+)\s?(?:horas|hora|h)\b\s?)?
    (\b(?P<minutes>\d+)\s?(?:minutos|minuto|min|m)\b\s?)?
    (\b(?P<seconds>\d+)\s?(?:segundos|segundo|seg|s)\b\s?)?
    """,
    re.VERBOSE,
)

pattern_absolute_time_and_date = re.compile(
    r"""
    (?:on|em)\s
    (?:\b
        (?P<hour>[01]?[0-9]|2[0-3])
        [h:]
        (?P<minute>[0-5][0-9])?
        :?
        (?P<second>[0-5][0-9])?
    \b\s?)?
    (?:\b
        (?P<day>0?[1-9]|[12][0-9]|3[01])
        [\/-]
        (?P<month>0?[1-9]|1[012])
        (?:[\/-](?P<year>[0-9]{4}))?
    \b\s?)?
    """,
    re.VERBOSE,
)


def birthday(target: str) -> Optional[str]:
    if "ano" in target and not any(x in target for x in ["mês", "meses", "semana", "dia"]):
        return " ".join(target.split()[:2])


def clean(target: Union[datetime, timedelta]) -> Union[datetime, str]:
    if isinstance(target, timedelta):
        return str(target).split(".")[0]
    if isinstance(target, datetime):
        return target.replace(tzinfo=timezone.utc).replace(microsecond=0)


def date_in_full(delta: timedelta) -> str:
    y, d = divmod(delta.days, 365)
    M, d = divmod(d, 30)
    m, s = divmod(delta.seconds, 60)
    H, m = divmod(m, 60)
    response = ""
    for value, unit in zip([y, M, d], ["ano", "mês", "dia"]):
        if value:
            unit = unit if value == 1 else "meses" if unit == "mês" else unit + "s"
            response += f"{value} {unit} "
    response += f"{H:02d}:{m:02d}:{s:02d}"
    return response.rstrip(", ")


def find_relative_time(target: str) -> Optional[re.Match]:
    match = pattern_relative_time.match(target)
    if match and any(match.groups()[1:]):
        return match


def find_absolute_time(target: str) -> Optional[re.Match]:
    match = pattern_absolute_time_and_date.match(target)
    if match and any(match.groups()[1:]):
        return match


def format(target: datetime) -> str:
    return (target - timedelta(hours=3)).strftime("%d/%m/%y às %H:%M:%S")


def on_cooldown(target: datetime, now: datetime = None, s: int = 0) -> Optional[timedelta]:
    now = now or datetime.utcnow()
    delta = clean(now) - clean(target)
    if delta.total_seconds() <= s:
        return timedelta(seconds=s) - delta


def timeago(target: datetime, now: datetime = None, full: bool = True) -> Union[str, timedelta]:
    now = now or datetime.utcnow()
    delta = clean(now) - clean(target)
    if full:
        return date_in_full(delta)
    return delta
