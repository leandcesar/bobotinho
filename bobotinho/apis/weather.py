# -*- coding: utf-8 -*-
from pyowm import OWM
from pyowm.utils.config import get_default_config

from bobotinho import config


config_dict = get_default_config()
config_dict["language"] = "pt_br"

owm = OWM(config.weather_key, config_dict)
Weather = owm.weather_manager()
