# -*- coding: utf-8 -*-
from typing import Optional

from bobotinho import aiorequests, config


class Currency:
    base_url = config.currency_url
    key = config.currency_key

    @classmethod
    async def conversion(cls, base: str, target: str) -> Optional[float]:
        url = f"{cls.base_url}/{cls.key}/latest/{base.upper()}"
        response = await aiorequests.get(url)
        rates = response.get("conversion_rates", {})
        rate = rates.get(target.upper())
        return rate
