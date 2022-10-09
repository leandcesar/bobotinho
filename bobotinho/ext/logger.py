# -*- coding: utf-8 -*-
import logging
import logging.config

__all__ = ("logger",)


logging.config.fileConfig("logging_config.ini")
logger = logging.getLogger()
