# -*- coding: utf-8 -*-
from typing import Optional

from bobotinho import aiorequests
from bobotinho.logger import log


class ColorAPI:
    base_url = "https://www.thecolorapi.com"

    @classmethod
    async def name(cls, color: str) -> Optional[str]:
        url = f"{cls.base_url}/id"
        params = {"hex": color}
        try:
            response = await aiorequests.get(url, params=params)
            color = response.get("name", {})
            color_name = color.get("value")
            return color_name
        except Exception as e:
            log.exception(e)
