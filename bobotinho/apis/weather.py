# -*- coding: utf-8 -*-
from pyowm import OWM
from bobotinho import config

Weather = OWM(config.weather_key, language="pt")
