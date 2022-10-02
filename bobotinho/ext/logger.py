# -*- coding: utf-8 -*-
import logging
import logging.config


logging.config.fileConfig("logging_config.ini")
logger = logging.getLogger()
