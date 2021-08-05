# -*- coding: utf-8 -*-
from typing import Optional

from bobotinho import aiorequests, config


class Crypto:
    base_url = config.crypto_url
    key = config.crypto_key

    @classmethod
    async def conversion(cls, base: str, target: str) -> Optional[float]:
        url = f"{cls.base_url}/{base.upper()}/{target.upper()}"
        headers = {"X-CoinAPI-Key": cls.key}
        response = await aiorequests.get(url, headers=headers)
        rate = response.get("rate")
        return rate
