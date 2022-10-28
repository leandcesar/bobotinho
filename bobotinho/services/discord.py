# -*- coding: utf-8 -*-
from aiohttp import ClientSession

__all__ = ("Discord",)


class Discord:
    def __init__(self, *, url: str, session: ClientSession = None) -> None:
        self.url = url
        self.session = session or ClientSession(raise_for_status=False)

    async def close(self) -> None:
        await self.session.close()

    async def webhook(self, *, name: str, content: str, avatar: str = None) -> bool:
        async with self.session.post(
            url=self.url,
            json={"username": name, "content": content, "avatar_url": avatar},
        ) as response:
            return response.ok
        return False
