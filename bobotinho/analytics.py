# -*- coding: utf-8 -*-
from aiohttp import ClientSession


class Analytics:
    url: str = "https://tracker.dashbot.io/track"
    session: ClientSession = ClientSession()

    def __init__(self, key: str) -> None:
        self.key = key

    async def track(self, type: str, user_id: int, text: str, **kwargs) -> bool:
        if not self.key:
            return False

        params = {
            "v": "11.1.0-rest",
            "platform": "universal",
            "apiKey": self.key,
            "type": type,
        }
        data = {
            "userId": user_id,
            "text": text,
            "intent": {
                "name": kwargs.get("intent"),
                "confidence": kwargs.get("confidence"),
            },
            # "images": [],
            # "buttons": [{"id": 1, "label": "text 1"}],
            "platformUserJson": {
                "firstName": kwargs.get("author"),
                "locale": kwargs.get("locale"),
                "plataform": kwargs.get("plataform"),
                "timezone": kwargs.pop("timezone", "-3"),
                "gender": kwargs.pop("gender", None),
            },
            "platformJson": kwargs.pop("extra", {}),
        }

        async with self.session.request("post", self.url, params=params, json=data) as response:
            return response.ok
        return False

    async def received(self, *, user_id: int, user_name: str, channel_name: str, content: str, **kwargs) -> bool:
        return await self.track("incoming", user_id, content, author=user_name, locale=channel_name, **kwargs)

    async def sent(self, *, user_id: int, user_name: str, channel_name: str, content: str, **kwargs) -> bool:
        return await self.track("outgoing", user_id, content, author=user_name, locale=channel_name, **kwargs)
