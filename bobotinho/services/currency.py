# -*- coding: utf-8 -*-
from string import ascii_uppercase

from aiohttp import ClientSession

__all__ = ("Currency",)


class Currency:
    def __init__(self, *, key: str, session: ClientSession = None) -> None:
        self.key = key
        self.session = session or ClientSession(raise_for_status=True)

    async def close(self) -> None:
        await self.session.close()

    async def rate(self, *, base: str, quote: str) -> float:
        base = base.upper()
        quote = quote.upper()
        if not (len(base) == 3 and all([x in ascii_uppercase for x in base])):
            raise ValueError(f"Invalid base '{base}'")
        if not (len(quote) == 3 and all([x in ascii_uppercase for x in quote])):
            raise ValueError(f"Invalid quote '{quote}'")
        async with self.session.get(
            url=f"https://rest.coinapi.io/v1/exchangerate/{base}/{quote}",
            headers={"x-coinapi-key": self.key},
        ) as response:
            data = await response.json()
            return data["rate"]
