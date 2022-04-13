# -*- coding: utf-8 -*-
from bobotinho import aiorequests


class Analytics:
    url = "https://tracker.dashbot.io/track"

    def __init__(self, key: str) -> None:
        self.key = key

    async def track(self, type: str, id: int, text: str, **kwargs):
        params = {
            "v": "11.1.0-rest",
            "platform": "universal",
            "apiKey": self.key,
            "type": type,
        }
        data = {
            "userId": id,
            "text": text,
            "intent": {
                "name": kwargs.get("intent"),
                "confidence": kwargs.get("confidence"),
            },
            # "images": [],
            # "buttons": [{"id": 1, "label": "text 1"}],
            "platformUserJson": {
                "firstName": kwargs.get("author"),
                "locale": kwargs.get("source"),
                "plataform": kwargs.get("plataform"),
                "timezone": kwargs.pop("timezone", "-3"),
                "gender": kwargs.pop("gender", None),
            },
            "platformJson": kwargs.pop("extra", {}),
        }
        await aiorequests.post(self.url, params=params, json=data, wait_response=False)

    async def received(self, ctx) -> None:
        await self.track(
            "incoming",
            id=ctx.author.id,
            text=ctx.message.content,
            author=ctx.author.name,
            source=ctx.channel.name,
        )

    async def sent(self, ctx) -> None:
        await self.track(
            "outgoing",
            id=ctx.author.id,
            text=ctx.response,
            author=ctx.author.name,
            source=ctx.channel.name,
        )
