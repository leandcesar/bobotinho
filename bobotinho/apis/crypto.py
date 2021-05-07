# -*- coding: utf-8 -*-
import os
from typing import Optional

from bobotinho import aiorequests
from bobotinho.logger import log


class CryptoAPI:
    base_url = "https://rest.coinapi.io/v1/exchangerate"
    key = os.getenv("API_KEY_CRYPTO")

    @classmethod
    async def conversion(cls, base: str, target: str) -> Optional[float]:
        url = f"{cls.base_url}/{base.upper()}/{target.upper()}"
        headers = {"X-CoinAPI-Key": cls.key}
        try:
            response = await aiorequests.get(url, headers=headers)
            rate = response.get("rate")
            return rate
        except Exception as e:
            log.exception(e)
