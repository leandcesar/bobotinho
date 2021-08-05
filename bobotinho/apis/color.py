# -*- coding: utf-8 -*-
from typing import Optional

from bobotinho import aiorequests, config


class Color:
    base_url = config.color_url

    @classmethod
    async def name(cls, color: str) -> Optional[str]:
        url = f"{cls.base_url}/id"
        params = {"hex": color}
        response = await aiorequests.get(url, params=params)
        color = response.get("name", {})
        color_name = color.get("value")
        return color_name
