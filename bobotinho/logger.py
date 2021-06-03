# -*- coding: utf-8 -*-
import logging
import os

key = os.getenv("API_KEY_BUGSNAG")

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(module)s.py (%(lineno)s) %(funcName)s: %(message)s",
)
log = logging.getLogger()

if os.getenv("CONFIG_MODE") == "prod":
    import bugsnag
    from bugsnag.handlers import BugsnagHandler

    try:
        bugsnag.configure(api_key=key, project_root="/bobotinho")
    except Exception as e:
        log.exception(e)
    else:
        handler = BugsnagHandler(extra_fields={"log": ["__repr__"]})
        handler.setLevel(logging.ERROR)
        log.addHandler(handler)
