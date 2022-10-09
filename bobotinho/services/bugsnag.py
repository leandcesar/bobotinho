# -*- coding: utf-8 -*-
import logging

import bugsnag
from bugsnag.handlers import BugsnagHandler

__all__ = ("bugsnag_handler",)

EXTRA_FIELDS = {"log": ["__repr__"], "locals": ["locals"], "ctx": ["ctx"]}


def bugsnag_handler(key: str, *, level: int = logging.ERROR, version: str = None, stage: str = None) -> logging.Handler:
    bugsnag.configure(api_key=key, app_version=version, release_stage=stage)
    handler = BugsnagHandler(extra_fields=EXTRA_FIELDS)
    handler.setLevel(level)
    return handler
