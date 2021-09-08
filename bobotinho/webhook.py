# -*- coding: utf-8 -*-
from bobotinho import aiorequests, config
from bobotinho.utils import discord
from bobotinho.exceptions import WebhookUrlNotDefined


class Webhook:
    @classmethod
    async def send(cls, url, **kwargs) -> None:
        data: dict = discord.embed(
            {
                "title": kwargs["title"],
                "description": kwargs["content"],
                "color": config.color_bot,
                "author_name": kwargs["author"],
                "footer_text": kwargs["source"],
                "timestamp": kwargs["timestamp"],
            }
        )
        await aiorequests.post(url, json=data, wait_response=False)

    @classmethod
    async def suggestions(cls, **kwargs) -> None:
        url: str = config.suggestions_webhook_url
        if not url:
            raise WebhookUrlNotDefined("suggestions")
        id: int = kwargs.pop("id")
        title: str = f"Sugestão #{id:04}"
        await cls.send(url, title=title, **kwargs)

    @classmethod
    async def bugs(cls, **kwargs) -> None:
        url: str = config.bugs_webhook_url
        if not url:
            raise WebhookUrlNotDefined("bugs")
        id: int = kwargs.pop("id")
        title: str = f"Bug #{id:04}"
        await cls.send(url, title=title, **kwargs)
