# -*- coding: utf-8 -*-
from bobotinho import aiorequests, config
from bobotinho.exceptions import WebhookUrlNotDefined


class Webhook:
    base_url: str = config.webhook_url
    timestamp_format: str = "%Y-%m-%dT%H:%M:%SZ"

    @classmethod
    async def send(cls, resource: str, **kwargs) -> None:
        if not cls.base_url:
            raise WebhookUrlNotDefined()
        data: dict = {
            "resource": resource,
            "data": kwargs,
        }
        await aiorequests.post(cls.url, json=data, wait_response=False)
