# -*- coding: utf-8 -*-
from bobotinho import aiorequests


class Api:
    url = "https://bobotinho.herokuapp.com"

    def __init__(self, token: str) -> None:
        self.token = token

    @property
    def headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}

    async def ping(self) -> bool:
        response = await aiorequests.get(f"{self.url}/ping", headers=self.headers)
        return response.status == 204

    async def color(self, hex_color: str) -> dict:
        response = await aiorequests.get(f"{self.url}/tools/color", params={"hex": hex_color}, headers=self.headers)
        return response["data"]

    async def currency(self, base: str, quote: str) -> float:
        response = await aiorequests.get(f"{self.url}/tools/currency", params={"base": base, "quote": quote}, headers=self.headers)
        return float(response["data"]["response"])

    async def dictionary(self, word: str) -> dict:
        response = await aiorequests.get(f"{self.url}/tools/dictionary", params={"word": word}, headers=self.headers)
        return response["data"]

    async def math(self, expression: str) -> str:
        response = await aiorequests.get(f"{self.url}/tools/math", params={"expression": expression}, headers=self.headers)
        return response["data"]["response"]

    async def translate(self, text: str, source: str, target: str) -> str:
        response = await aiorequests.get(f"{self.url}/tools/translate", params={"text": text, "source": source, "target": target}, headers=self.headers)
        return response["data"]["response"]

    async def twitch(self, infos: str, channel: str, user: str = None) -> dict:
        response = await aiorequests.get(f"{self.url}/tools/twitch", params={"infos": infos, "channel": channel, "user": user}, headers=self.headers)
        return response["data"]

    async def weather(self, location: str) -> dict:
        response = await aiorequests.get(f"{self.url}/tools/weather", params={"location": location}, headers=self.headers)
        return response["data"]

    async def joke(self) -> str:
        response = await aiorequests.get(f"{self.url}/random/joke", headers=self.headers)
        return response["data"]["response"]

    async def quote(self) -> str:
        response = await aiorequests.get(f"{self.url}/random/quote", headers=self.headers)
        return response["data"]["response"]

    async def sadcat(self) -> str:
        response = await aiorequests.get(f"{self.url}/random/sadcat", headers=self.headers)
        return response["data"]["response"]

    async def word(self) -> str:
        response = await aiorequests.get(f"{self.url}/random/word", headers=self.headers)
        return response["data"]["response"]
