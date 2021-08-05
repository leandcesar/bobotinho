# -*- coding: utf-8 -*-
import logging

from bobotinho import config

try:
    logging.basicConfig(
        level=config.log_level,
        format="[%(levelname)s] %(module)s.py:%(lineno)s: %(message)s",
    )
except ValueError:
    print(f"[ERROR] Invalid <LOG_LEVEL>. Not expected '{config.log_level}'")
    logging.basicConfig()
finally:
    log: logging.Logger = logging.getLogger()

if config.bugsnag_key:
    import bugsnag
    from bugsnag.handlers import BugsnagHandler

    try:
        bugsnag.configure(
            app_version=config.version,
            api_key=config.bugsnag_key,
            project_root="/bobotinho",
            release_stage=config.mode,
        )
        handler: BugsnagHandler = BugsnagHandler(
            extra_fields={"log": ["__repr__"], "ctx": ["ctx"]}
        )
        handler.setLevel(logging.ERROR)
    except Exception as e:
        log.exception(e)
    else:
        log.addHandler(handler)
