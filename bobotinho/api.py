# -*- coding: utf-8 -*-
from typing import Optional, Union

from aiohttp import ClientSession


class Api:
    site_url = "https://bobotinho.herokuapp.com"
    session = ClientSession()

    def __init__(self, key: str) -> None:
        self.key = key

    @property
    def headers(self) -> dict:
        return {"Authorization": f"Bearer {self.key}"}

    async def request(self, endpoint: str, method: str = "get", params: dict = {}) -> Optional[Union[bool, dict, str]]:
        async with self.session.request(
            method,
            f"{self.url}/{endpoint}",
            headers=self.headers,
            params={k: v for k, v in params.items() if v is not None},
        ) as response:
            if response.status == 204:
                return True
            if response.ok:
                data = await response.json()
                return data["data"].get("response") or data["data"]

    async def ping(self) -> Optional[bool]:
        return await self.request("ping")

    async def color(self, hex_color: str) -> Optional[dict]:
        return await self.request("tools/color", params={"hex": hex_color})

    async def currency(self, base: str, quote: str) -> Optional[str]:
        return await self.request("tools/currency", params={"base": base, "quote": quote})

    async def dictionary(self, word: str) -> Optional[dict]:
        return await self.request("tools/dictionary", params={"word": word})

    async def math(self, expression: str) -> Optional[str]:
        return await self.request("tools/math", params={"expression": expression})

    async def translate(self, text: str, source: str, target: str) -> Optional[str]:
        return await self.request("tools/translate", params={"text": text, "source": source, "target": target})

    async def twitch(self, infos: str, channel: str, user: str = None) -> Optional[dict]:
        return await self.request("tools/twitch", params={"infos": infos, "channel": channel, "user": user})

    async def weather(self, location: str) -> Optional[dict]:
        return await self.request("tools/weather", params={"location": location})

    async def joke(self) -> Optional[str]:
        return await self.request("random/joke")

    async def quote(self) -> Optional[str]:
        return await self.request("random/quote")

    async def sadcat(self) -> Optional[str]:
        return await self.request("random/sadcat")

    async def word(self) -> Optional[str]:
        return await self.request("random/word")
