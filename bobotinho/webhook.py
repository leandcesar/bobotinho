# -*- coding: utf-8 -*-
from bobotinho import aiorequests, config
from bobotinho.utils import discord
from bobotinho.exceptions import WebhookUrlNotDefined


class Webhook:
    @classmethod
    async def send(cls, url, resource: str, title: str, **kwargs) -> None:
        if not url:
            WebhookUrlNotDefined(resource)
        data: dict = discord.embed(
            {
                "title": title,
                "description": kwargs["content"],
                "color": config.color_bot,
                "author_name": "@{user}".format(user=kwargs["author"]),
                "author_url": "https://twitch.tv/{user}".format(user=kwargs["author"]),
                "footer_text": "@{user}".format(user=kwargs["channel"]),
                "timestamp": kwargs["timestamp"].strftime(discord.timestamp_format),
            }
        )
        await aiorequests.post(url, json=data, wait_response=False)

    @classmethod
    async def suggestions(cls, **kwargs) -> None:
        url: str = config.suggestions_webhook_url
        title: str = "Sugestão #{id:04}".format(id=kwargs.pop("id"))
        await cls.send(url, resource="suggestions", title=title, **kwargs)

    @classmethod
    async def bugs(cls, **kwargs) -> None:
        url: str = config.bugs_webhook_url
        title: str = "Bug #{id:04}".format(id=kwargs.pop("id"))
        await cls.send(url, resource="bugs", title=title, **kwargs)
