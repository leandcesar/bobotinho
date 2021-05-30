
# -*- coding: utf-8 -*-
import os
import time
from typing import Optional

from bobotinho import aiorequests
from bobotinho.logger import log


class Analytics:
    base_url = "https://chatbase.com/api"
    key = os.getenv("API_KEY_ANALYTICS")

    @classmethod
    async def received(cls, ctx, handled: bool) -> Optional[dict]:
        url = f"{cls.base_url}/message"
        data = {
            "api_key": cls.key,
            "version": "0.1.0",
            "platform": "Twitch",
            "type": "user",
            "user_id": ctx.author.id,
            "message": ctx.content,
            "time_stamp": int(time.time() * 1e3),
            "not_handled": not handled,
        }
        try:
            await aiorequests.post(url, json=data, wait_response=False, loop=ctx.bot.loop)
        except Exception as e:
            log.exception(e)

    @classmethod
    async def sent(cls, ctx, handled: bool) -> Optional[dict]:
        url = f"{cls.base_url}/message"
        data = {
            "api_key": cls.key,
            "version": "0.1.0",
            "platform": "Twitch",
            "type": "agent",
            "user_id": ctx.author.id,
            "message": ctx.response,
            "time_stamp": int(time.time() * 1e3),
            "not_handled": not handled,
        }
        try:
            await aiorequests.post(url, json=data, wait_response=False, loop=ctx.bot.loop)
        except Exception as e:
            log.exception(e)
