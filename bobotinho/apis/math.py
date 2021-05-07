# -*- coding: utf-8 -*-
from typing import Optional

from bobotinho import aiorequests
from bobotinho.logger import log


class MathAPI:
    base_url = "https://api.mathjs.org/v4"

    @classmethod
    async def calculate(cls, operation: str) -> Optional[str]:
        url = cls.base_url
        params = {"expr": operation, "precision": "4"}
        try:
            response = await aiorequests.get(url, params=params, res_method="text")
            return response
        except Exception as e:
            log.exception(e)
