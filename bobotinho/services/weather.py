# -*- coding: utf-8 -*-
from aiohttp import ClientSession

__all__ = ("Weather",)

CODE_EMOJI = {
    "01d": "🌞",
    "02d": "🌤",
    "03d": "☁️",
    "04d": "🌥",
    "09d": "🌧",
    "10d": "🌦",
    "11d": "⛈",
    "13d": "🌨",
    "50d": "🌫",
    "01n": "🌙",
    "02n": "🌤",
    "03n": "☁️",
    "04n": "🌥",
    "09n": "🌧",
    "10n": "🌦",
    "11n": "⛈",
    "13n": "🌨",
    "50n": "🌫",
}


class Weather:
    def __init__(self, *, key: str, session: ClientSession = None) -> None:
        self.key = key
        self.session = session or ClientSession(raise_for_status=True)

    async def close(self) -> None:
        await self.session.close()

    async def prediction(self, *, location: str, language: str = "pt_br", units: str = "metric") -> dict:
        async with self.session.get(
            url="https://api.openweathermap.org/data/2.5/weather",
            params={"appid": self.key, "lang": language, "units": units, "q": location},
        ) as response:
            data = await response.json()
            new_data = {}
            for key, value in data.items():
                if isinstance(value, dict):
                    new_data = {**value, **new_data}
                elif isinstance(value, list):
                    new_data = {**value[0], **new_data}
                else:
                    new_data = {key: value, **new_data}
            if "all" in new_data:
                new_data["clouds"] = new_data.pop("all")
            if "feels_like" in new_data:
                new_data["temp_feels_like"] = new_data.pop("feels_like")
            if "icon" in new_data:
                new_data["emoji"] = CODE_EMOJI.get(new_data.pop("icon"), "🌤")
            return new_data
