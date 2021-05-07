# -*- coding: utf-8 -*-
import os
from pyowm import OWM

WeatherAPI = OWM(os.getenv("API_KEY_WEATHER"), language="pt")
