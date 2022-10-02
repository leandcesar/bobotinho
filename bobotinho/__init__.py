# -*- coding: utf-8 -*-
from bobotinho.ext.config import config
from bobotinho.ext.logger import logger
from bobotinho.services.bugsnag import bugsnag_handler

__title__ = "bobotinho"
__author__ = "Leandro César"
__license__ = "GNU"
__copyright__ = "Copyright 2020 bobotinho"
__version__ = config.version

try:
    if config.bugsnag_key is None:
        raise KeyError("'BUGSNAG_KEY' env var not set, couldn't notify")
    handler = bugsnag_handler(key=config.bugsnag_key, version=config.version, stage=config.stage)
except Exception as error:
    logger.warning(error)
else:
    logger.addHandler(handler)
