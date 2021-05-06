# -*- coding: utf-8 -*-
import logging


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(module)s.py (%(lineno)s) %(funcName)s: %(message)s",
)

log = logging.getLogger()
