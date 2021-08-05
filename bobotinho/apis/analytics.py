# -*- coding: utf-8 -*-
from bobotinho import aiorequests, config


class Analytics:
    base_url = config.analytics_url
    key = config.analytics_key

    @classmethod
    async def request(cls, type: str, loop, **kwargs):
        url = f"{cls.base_url}?v=11.1.0-rest&platform=universal&apiKey={cls.key}&type={type}"
        data = {
            "text": kwargs["text"],
            "userId": kwargs["id"],
            "intent": {"name": kwargs.get("intent"), "confidence": kwargs.get("confidence")},
            "platformUserJson": {"firstName": kwargs.get("name")},
            "platformJson": {"source": "Twitch", "channel": kwargs.get("channel")},
        }
        await aiorequests.post(url, json=data, wait_response=False, loop=loop)

    @classmethod
    async def received(cls, loop, **kwargs) -> None:
        await cls.request("incoming", loop, **kwargs)

    @classmethod
    async def sent(cls, loop, **kwargs) -> None:
        await cls.request("outgoing", loop, **kwargs)
