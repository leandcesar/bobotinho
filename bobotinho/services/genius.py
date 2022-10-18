# -*- coding: utf-8 -*-
import html
from aiohttp import ClientSession, TCPConnector

__all__ = ("Genius",)


class Utils:

    @staticmethod
    def remove_tags(page: str) -> str:
        page = page.replace("<br/>", "\n")
        new_text = ""
        tag = False
        for char in page:
            if not tag and char == "<":
                tag = True
            elif not tag:
                new_text += char
            elif tag and char == ">":
                tag = False
        return new_text


class Genius:
    def __init__(self, *, key: str, session: ClientSession = None) -> None:
        self.key = key
        self.session = session or ClientSession(
            connector=TCPConnector(limit=50),
            headers={"Authorization": f"Bearer {self.key}"},
            conn_timeout=None,
            read_timeout=None,
            raise_for_status=False,
        )

    async def close(self) -> None:
        pass

    async def get_lyrics(self, *, title: str, artist: str) -> dict:
        async with self.session.get(
            url="https://api.genius.com/search",
            params={"q": f"{title} {artist}".lower().replace("ao vivo", "")}
        ) as response:
            data = await response.json()
            lyrics_url = data["response"]["hits"][0]["result"]["url"]
            if not lyrics_url.endswith("lyrics"):
                return None

        async with self.session.get(url=lyrics_url) as response:
            data = await response.text()

        page = html.unescape(data)
        page = page[page.find('<div class="LyricsControls__Flex'):]
        page = page[:page.find('<div class="Lyrics__Footer')]
        lyrics = Utils.remove_tags(page)
        return lyrics
