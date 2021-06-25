# -*- coding: utf-8 -*-
import os


def resetting_daily() -> bool:
    return os.getenv("RESETTING_DAILY") == "1"
