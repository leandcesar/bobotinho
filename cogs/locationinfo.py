# -*- coding: utf-8 -*-

"""
bobotinho - Twitch bot for Brazilian offstream chat entertainment
Copyright (C) 2020  Leandro César

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import config
import json
import pyowm
import re
import string

from ext.command import command
from twitchio.ext import commands
from unidecode import unidecode
from utils import asyncrq, convert

countries = json.load(open("data//countries.json", "r", encoding="utf-8"))
emojis = {
    "aguaceiros": "⛈",
    "céu limpo": "🌞",
    "céu pouco nublado": "🌤",
    "chuva forte": "🌧️",
    "chuva fraca": "🌦",
    "chuva muito forte": "⛈",
    "chuvisco": "☔",
    "fumo": "🌫",
    "névoa": "🌫",
    "nevoeiro": "🌫",
    "nublado": "☁️",
    "nuvens dispersas": "⛅",
    "nuvens quebradas": "🌥",
    "trovoada": "⛈",
}


class LocationInfo(commands.AutoCog):
    def __init__(self, bot):
        self.bot = bot
        self.owm = pyowm.OWM(config.Vars.apikey_owm, language="pt")

    def _prepare(self, bot):
        pass

    @command(description="saiba o clima atual de alguma cidade", usage="digite o comando e o nome de um local para saber o clima")
    async def weather(self, ctx, *, location: str):
        location = location.translate(str.maketrans("", "", string.punctuation))
        if " " in location and location.rsplit(maxsplit=1)[-1].lower() in (tuple(countries)):
            location, country = location.rsplit(maxsplit=1)
            location = location + ", " + country.upper()

        try:
            observation = await self.bot.loop.run_in_executor(
                None, self.owm.weather_at_place, location
            )
        except:
            ctx.response = f"@{ctx.author.name}, não há nenhuma previsão para esse local"
        else:
            city = observation.get_location().get_name()
            country = observation.get_location().get_country()
            weather = observation.get_weather()
            status = weather.get_detailed_status()
            temp = weather.get_temperature("celsius")["temp"]
            wind = weather.get_wind()["speed"]
            humidiy = weather.get_humidity()
            emoji = emojis.get(status, "☁️")
            ctx.response = (
                f"@{ctx.author.name}, em {city} ({country}): {emoji} {status}, "
                f"{temp}°C, ventos a {wind}m/s e {humidiy}% de umidade"
            )

    
def prepare(bot):
    bot.add_cog(LocationInfo(bot))


def breakdown(bot):
    pass
