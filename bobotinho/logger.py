# -*- coding: utf-8 -*-
import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="[%(levelname)s] %(module)s.py:%(lineno)s %(funcName)s: %(message)s",
)
log = logging.getLogger()

if os.getenv("CONFIG_MODE") == "prod":
    import bugsnag
    from bugsnag.handlers import BugsnagHandler

    try:
        bugsnag.configure(
            api_key=os.getenv("API_KEY_BUGSNAG"),
            project_root="/bobotinho",
        )
    except Exception as e:
        log.exception(e)
    else:
        handler = BugsnagHandler(extra_fields={"log": ["__repr__"]})
        handler.setLevel(logging.ERROR)
        log.addHandler(handler)
