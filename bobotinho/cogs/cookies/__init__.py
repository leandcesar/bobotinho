# -*- coding: utf-8 -*-
import os


def resetting_daily() -> bool:
    return os.environ.get("RESETTING_DAILY") == "1"
