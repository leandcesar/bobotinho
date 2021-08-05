# -*- coding: utf-8 -*-
from typing import Optional

from bobotinho import aiorequests, config


class Math:
    base_url = config.math_url

    @classmethod
    async def calculate(cls, operation: str) -> Optional[str]:
        url = cls.base_url
        params = {"expr": operation, "precision": "4"}
        response = await aiorequests.get(url, params=params, res_method="text")
        return response
