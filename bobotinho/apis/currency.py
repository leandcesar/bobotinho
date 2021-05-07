# -*- coding: utf-8 -*-
import os
from typing import Optional

from bobotinho import aiorequests
from bobotinho.logger import log


class CurrencyAPI:
    base_url = "https://v6.exchangerate-api.com/v6"
    key = os.getenv("API_KEY_CURRENCY")

    @classmethod
    async def conversion(cls, base: str, target: str) -> Optional[float]:
        url = f"{cls.base_url}/{cls.key}/latest/{base.upper()}"
        try:
            response = await aiorequests.get(url)
            rates = response.get("conversion_rates", {})
            rate = rates.get(target.upper())
            return rate
        except Exception as e:
            log.exception(e)
