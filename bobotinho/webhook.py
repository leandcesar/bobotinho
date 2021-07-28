# -*- coding: utf-8 -*-
import os

from bobotinho import aiorequests


class Webhook:
    url = os.getenv("BOT_NOTIFIER_URL")
    timestamp_format = "%Y-%m-%dT%H:%M:%SZ"

    @classmethod
    async def send(cls, resource, **kwargs) -> None:
        if not cls.url:
            return
        data = {
            "resource": resource,
            "data": kwargs,
        }
        await aiorequests.post(cls.url, json=data, wait_response=False)
