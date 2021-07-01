
# -*- coding: utf-8 -*-
import os
from typing import Optional

from bobotinho import aiorequests
from bobotinho.logger import log


class Analytics:
    base_url = "https://tracker.dashbot.io/track"
    key = os.getenv("API_KEY_ANALYTICS")
    nick = os.getenv("BOT_NAME")

    @classmethod
    async def received(cls, ctx) -> Optional[dict]:
        log.debug(f"#{ctx.channel.name} @{ctx.author.name}: {ctx.content}")
        url = f"{cls.base_url}?v=11.1.0-rest&platform=universal&apiKey={cls.key}&type=incoming"
        data = {
            "text": ctx.content,
            "userId": ctx.author.id,
            "platformUserJson": {"firstName": ctx.author.name},
            "platformJson": {"source": "Twitch", "channel": ctx.channel.name},
        }
        try:
            await aiorequests.post(url, json=data, wait_response=False, loop=ctx.bot.loop)
        except Exception as e:
            log.exception(e)

    @classmethod
    async def sent(cls, ctx) -> Optional[dict]:
        log.debug(f"#{ctx.channel.name} @{cls.nick}: {ctx.response}")
        url = f"{cls.base_url}?v=11.1.0-rest&platform=universal&apiKey={cls.key}&type=outgoing"
        data = {
            "text": ctx.response,
            "userId": ctx.author.id,
            "intent": {"name": ctx.command.name, "confidence": 1.0},
            "platformUserJson": {"firstName": ctx.author.name},
            "platformJson": {"source": "Twitch", "channel": ctx.channel.name},
        }
        try:
            await aiorequests.post(url, json=data, wait_response=False, loop=ctx.bot.loop)
        except Exception as e:
            log.exception(e)
