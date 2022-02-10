# -*- coding: utf-8 -*-
from bobotinho import aiorequests, config


class Analytics:
    base_url = config.analytics_url
    key = config.analytics_key

    @classmethod
    async def request(cls, type: str, **kwargs):
        url = f"{cls.base_url}?v=11.1.0-rest&platform=universal&apiKey={cls.key}&type={type}"
        data = {
            "text": kwargs["content"],
            "userId": kwargs["id"],
            "intent": {
                "name": kwargs.get("intent"),
                "confidence": kwargs.get("confidence"),
            },
            "platformUserJson": {
                "firstName": kwargs.get("author"),
                "locale": kwargs.get("source"),
                "plataform": kwargs.get("plataform"),
            },
        }
        await aiorequests.post(url, json=data, wait_response=False)

    @classmethod
    async def received(cls, ctx) -> None:
        await cls.request(
            "incoming",
            id=ctx.author.id,
            content=ctx.message.content,
            author=ctx.author.name,
            source=ctx.channel.name,
            plataform=ctx.bot.plataform,
        )

    @classmethod
    async def sent(cls, ctx) -> None:
        await cls.request(
            "outgoing",
            id=ctx.author.id,
            content=ctx.response,
            author=ctx.author.name,
            source=ctx.channel.name,
            plataform=ctx.bot.plataform,
        )
