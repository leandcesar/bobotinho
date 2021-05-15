# -*- coding: utf-8 -*-
import os

from bobotinho import aiorequests


class Webhook:
    url = os.getenv("WEBHOOK_URL")
    timestamp_format = "%Y-%m-%dT%H:%M:%SZ"

    @classmethod
    async def suggestions(cls, suggest):
        data = {
            "app": "bobotinho-bot",
            "resource": "suggestions",
            "id": suggest.id,
            "content": suggest.content,
            "author": suggest.name,
            "channel": suggest.channel,
            "timestamp": suggest.updated_at.strftime(cls.timestamp_format),
        }
        await aiorequests.post(cls.url, json=data)

    @classmethod
    async def status(cls, systemlog, created):
        data = {
            "app": "bobotinho-bot",
            "resource": "status",
            "id": systemlog.id,
            "status": created,
            "error": systemlog.error,
            "timestamp": systemlog.updated_at.strftime(cls.timestamp_format),
        }
        await aiorequests.post(cls.url, json=data)
