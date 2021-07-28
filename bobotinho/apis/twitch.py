# -*- coding: utf-8 -*-
from typing import Optional

from bobotinho import aiorequests
from bobotinho.logger import log


class TwitchAPI:
    base_url = "https://decapi.me/twitch"
    errors = [
        "Error", "Not Found", "not follow", "be specified", "No user", "not found", "cannot follow", "not have"
    ]

    @classmethod
    async def request(cls, endpoint: str) -> Optional[str]:
        url = f"{cls.base_url}/{endpoint}"
        params = {
            "lang": "pt",
            "precision": "3",
            "format": "d/m/Y \\à\\s H:i:s",
            "tz": "America/Sao_Paulo",
            "direction": "asc",
            "count": "1",
            "limit": "2",
        }
        try:
            response = await aiorequests.get(url, params=params, res_method="text")
            if response.startswith("No user with the name"):
                name = response.split('"')[1]
                return f"@{name} não existe"
            if not any(e in response for e in cls.errors):
                if endpoint.startswith(("following", "followers")):
                    return response.split(", ")[0]
                return response
        except Exception as e:
            log.exception(e)

    @classmethod
    async def account_age(cls, name: str) -> Optional[str]:
        return await cls.request(f"accountage/{name}")

    @classmethod
    async def avatar(cls, name: str) -> Optional[str]:
        return await cls.request(f"avatar/{name}")

    @classmethod
    async def creation(cls, name: str) -> Optional[str]:
        return await cls.request(f"creation/{name}")

    @classmethod
    async def follow_age(cls, channel: str, name: str) -> Optional[str]:
        return await cls.request(f"followage/{channel}/{name}")

    @classmethod
    async def follow_count(cls, name: str) -> Optional[str]:
        return await cls.request(f"followcount/{name}")

    @classmethod
    async def followed(cls, channel: str, name: str) -> Optional[str]:
        return await cls.request(f"followed/{channel}/{name}")

    @classmethod
    async def followers(cls, channel: str) -> Optional[str]:
        return await cls.request(f"followers/{channel}")

    @classmethod
    async def following(cls, name: str) -> Optional[str]:
        return await cls.request(f"following/{name}")

    @classmethod
    async def game(cls, name: str) -> Optional[str]:
        return await cls.request(f"game/{name}")

    @classmethod
    async def title(cls, name: str) -> Optional[str]:
        return await cls.request(f"title/{name}")

    @classmethod
    async def total_views(cls, name: str) -> Optional[str]:
        return await cls.request(f"total_views/{name}")

    @classmethod
    async def uptime(cls, name: str) -> Optional[str]:
        return await cls.request(f"uptime/{name}")

    @classmethod
    async def viewer_count(cls, name: str) -> Optional[str]:
        return await cls.request(f"viewercount/{name}")
