# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

YEAR = "ano"
DAY = "dia"
HOUR = "hora"
MINUTE = "minuto"
SECOND = "segundo"
YY = "a"
DD = "d"
HH = "h"
MM = "min"
SS = "s"


class timeago:
    def __init__(self, target: datetime, *, now: datetime = None) -> None:
        if now is None:
            now = datetime.utcnow()
        target = target.replace(tzinfo=None)
        now = now.replace(tzinfo=None)
        if target > now:
            raise ValueError()

        delta = now - target
        yy, dd = divmod(delta.days, 365)
        mm, ss = divmod(delta.seconds, 60)
        hh, mm = divmod(mm, 60)
        self.years = yy
        self.days = dd
        self.hours = hh
        self.minutes = mm
        self.seconds = ss

    def humanize(self, *, precision: int = 1, minimum: str = SS, short: bool = False) -> str:
        quote = ""
        for value, name, symbol in [
            (self.years, YEAR, YY),
            (self.days, DAY, DD),
            (self.hours, HOUR, HH),
            (self.minutes, MINUTE, MM),
            (self.seconds, SECOND, SS),
        ]:
            if value <= 0:
                continue
            if symbol > minimum:
                continue
            if len(quote.split()) >= precision * (int(not short) + 1):
                break
            unit = symbol if short else f" {name}"
            plural = "s" if value != 1 and not short else ""
            quote += f" {value}{unit}{plural}"
        quote = quote.strip()
        if quote:
            return " ".join(quote.split()[: 2 * precision])
        return "pouco tempo"
