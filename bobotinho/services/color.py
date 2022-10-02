# -*- coding: utf-8 -*-
from string import hexdigits

from aiohttp import ClientSession


class Color:
    def __init__(self, *, session: ClientSession = None) -> None:
        self.session = session or ClientSession(raise_for_status=True)

    async def close(self) -> None:
        await self.session.close()

    async def hex_to_name(self, *, code: str) -> str:
        code = code.replace("#", "").upper()
        if not (len(code) == 6 and all([x in hexdigits for x in code])):
            raise ValueError(f"Invalid hex code '{code}'")
        async with self.session.request(
            "get",
            url="https://www.thecolorapi.com/id",
            params={"hex": code},
        ) as response:
            data = await response.json()
            return data["name"]["value"]
