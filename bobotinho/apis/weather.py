# -*- coding: utf-8 -*-
from pyowm import OWM
from pyowm.utils.config import get_default_config

from bobotinho import config, log

try:
    config_dict = get_default_config()
    config_dict["language"] = "pt_br"
    owm = OWM(config.weather_key, config_dict).weather_manager()
except Exception as e:
    log.warning(e)


class Weather:
    @staticmethod
    def predict(place: str) -> dict:
        observation = owm.weather_at_place(place)
        location = observation.location
        weather = observation.weather
        celsius = weather.temperature("celsius")
        wind = weather.wind()
        return {
            "city": location.name,
            "country": location.country,
            "status": weather.detailed_status,
            "temperature": celsius["temp"],
            "feels_like": celsius["feels_like"],
            "wind": wind["speed"],
            "humidiy": weather.humidity,
        }
