# -*- coding: utf-8 -*-
from typing import Optional, Tuple

from aiohttp import ClientSession

__all__ = ("WitAI",)


class WitAI:
    def __init__(self, *, key_duration: str, key_datetime: str, session: ClientSession = None) -> None:
        self.key_duration = key_duration
        self.key_datetime = key_datetime
        self.session = session or ClientSession(raise_for_status=False)

    async def close(self) -> None:
        await self.session.close()

    async def get_duration(self, *, message: str) -> Tuple[Optional[str], Optional[int]]:
        async with self.session.get(
            "https://api.wit.ai/message",
            headers={"Authorization": f"Bearer {self.key_duration}"},
            params={"v": 1, "q": message}
        ) as response:
            data = await response.json()

        try:
            seconds = 0
            start = len(message)
            end = 0
            for duration in data["entities"]["wit$duration:duration"]:
                seconds += duration["normalized"]["value"]
                if duration["start"] < start:
                    start = duration["start"]
                if duration["end"] > end:
                    end = duration["end"]
            text = message[start:end]
            return text, seconds
        except KeyError:
            return None, None

    async def get_datetime(self, *, message: str) -> Tuple[Optional[str], Optional[str]]:
        async with self.session.get(
            "https://api.wit.ai/message",
            headers={"Authorization": f"Bearer {self.key_datetime}"},
            params={"v": 1, "q": message}
        ) as response:
            data = await response.json()

        try:
            date_string = data["entities"]["wit$datetime:datetime"][0]["value"]
            text = data["entities"]["wit$datetime:datetime"][0]["body"]
            return text, date_string
        except KeyError:
            return None, None
