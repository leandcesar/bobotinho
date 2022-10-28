# -*- coding: utf-8 -*-
from aiohttp import ClientSession

__all__ = ("Dashbot",)


class Dashbot:
    def __init__(self, *, key: str, session: ClientSession = None) -> None:
        self.key = key
        self.session = session or ClientSession(raise_for_status=False)

    async def close(self) -> None:
        await self.session.close()

    async def track(self, *, echo: bool, id: int, message: str, **kwargs) -> bool:
        _type = "outgoing" if echo else "incoming"
        async with self.session.post(
            url="https://tracker.dashbot.io/track",
            params={
                "v": "11.1.0-rest",
                "platform": "universal",
                "apiKey": self.key,
                "type": _type,
            },
            json={
                "userId": id,
                "text": message,
                "intent": {
                    "name": kwargs.get("intent"),
                    "confidence": kwargs.get("confidence"),
                },
                "platformUserJson": {
                    "firstName": kwargs.get("name"),
                    "locale": kwargs.get("locale"),
                    "plataform": kwargs.get("plataform"),
                    "timezone": kwargs.get("timezone", "-3"),
                    "gender": kwargs.get("gender"),
                },
                "platformJson": kwargs.get("extra", {}),
            },
        ) as response:
            return response.ok
        return False

    async def received(self, *, id: int, name: str, message: str, **kwargs) -> bool:
        return await self.track(echo=False, id=id, name=name, message=message, **kwargs)

    async def sent(self, *, id: int, name: str, message: str, **kwargs) -> bool:
        return await self.track(echo=True, id=id, name=name, message=message, **kwargs)
