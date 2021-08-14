# -*- coding: utf-8 -*-
timestamp_format: str = "%Y-%m-%dT%H:%M:%SZ"


def embed(data: dict) -> dict:
    return {
        "embeds": [
            {
                "title": data.get("title"),
                "url": data.get("url"),
                "description": data.get("description"),
                "color": data.get("color"),
                "thumbnail": {"url": data.get("thumbnail")},
                "image": {"url": data.get("image")},
                "author": {
                    "name": data.get("author_name"),
                    "icon_url": data.get("author_icon_url"),
                    "url": data.get("author_url"),
                },
                "footer": {
                    "text": data.get("footer_text"),
                    "icon_url": data.get("footer_icon_url"),
                },
                "timestamp": data.get("timestamp"),
            }
        ]
    }
