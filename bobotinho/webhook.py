# -*- coding: utf-8 -*-
import os

from bobotinho import aiorequests


class Webhook:
    url = os.getenv("BOT_NOTIFIER_URL")
    app = "bobotinho-bot"
    timestamp_format = "%Y-%m-%dT%H:%M:%SZ"

    @classmethod
    async def suggestions(cls, suggest) -> None:
        if not cls.url:
            return
        data = {
            "app": cls.app,
            "resource": "suggestions",
            "id": suggest.id,
            "content": suggest.content,
            "author": suggest.name,
            "channel": suggest.channel,
            "timestamp": suggest.updated_at.strftime(cls.timestamp_format),
        }
        await aiorequests.post(cls.url, json=data, wait_response=False)
