# -*- coding: utf-8 -*-
from aiohttp import ClientSession


class Webhook:
    session = ClientSession()

    async def discord(self, url: str, *, content: str, user_name: str = None, user_avatar_url: str = None) -> bool:
        data = {
            "username": user_name,
            "avatar_url": user_avatar_url,
            "content": content,
        }
        async with self.session.request("post", url, json=data) as response:
            return response.ok
