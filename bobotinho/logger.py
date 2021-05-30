# -*- coding: utf-8 -*-
import logging
import os

import bugsnag
from bugsnag.handlers import BugsnagHandler

key = os.getenv("API_KEY_BUGSNAG")

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(module)s.py (%(lineno)s) %(funcName)s: %(message)s",
)
log = logging.getLogger()

try:
    bugsnag.configure(api_key=key, project_root="/bobotinho")
except Exception as e:
    log.exception(e)
else:
    handler = BugsnagHandler()
    handler.setLevel(logging.ERROR)
    log.addHandler(handler)
