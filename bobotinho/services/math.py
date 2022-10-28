# -*- coding: utf-8 -*-
from aiohttp import ClientSession

__all__ = ("Math",)


class Math:
    def __init__(self, *, session: ClientSession = None) -> None:
        self.session = session or ClientSession(raise_for_status=True)

    async def close(self) -> None:
        await self.session.close()

    async def evaluate(self, *, expression: str, precision: int = 4) -> str:
        async with self.session.post(
            url="https://api.mathjs.org/v4",
            json={"expr": expression, "precision": precision},
        ) as response:
            data = await response.json()
            return data["result"]
