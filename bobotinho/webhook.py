# -*- coding: utf-8 -*-
from datetime import datetime

from bobotinho import aiorequests


def to_embed(timestamp: bool = True, **kwargs):
    data = {
        "username": kwargs.get("name"),
        "avatar_url": kwargs.get("icon_url"),
        "content": kwargs.get("text"),
        "embeds": [
            {
                "author": {
                    "name": kwargs.get("author_name"),
                    "url": kwargs.get("author_url"),
                    "icon_url": kwargs.get("author_icon_url"),
                },
                "title": kwargs.get("title"),
                "url": kwargs.get("url"),
                "description": kwargs.get("description"),
                "color": kwargs.get("color"),
                "fields": kwargs.get("fields"),  # fields = [{"name": str, "value": str, "inline": bool}, ...]
                "thumbnail": {
                    "url": kwargs.get("thumbnail"),
                },
                "image": {
                    "url": kwargs.get("image"),
                },
                "footer": {
                    "text": kwargs.get("footer_text"),
                    "icon_url": kwargs.get("footer_icon_url"),
                },
                "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") if timestamp else None,
            },
        ],
    }
    
    def remove_none(data: dict):
        return (
            type(data)(remove_none(x) for x in data if x)
            if isinstance(data, (list, tuple, set))
            else type(data)((remove_none(k), remove_none(v)) for k, v in data.items() if k and v)
            if isinstance(data, dict)
            else data
        )

    data = remove_none(data)
    return data


class Webhook:

    @staticmethod
    async def discord(url: str, payload: dict) -> None:
        await aiorequests.post(url, json=to_embed(**payload), wait_response=False)
