# -*- coding: utf-8 -*-
__title__ = "bobotinho-bot"
__author__ = "Leandro César"
__license__ = "GNU"
__copyright__ = "Copyright 2020 bobotinho"
__version__ = "0.1.0"

import asyncio
import os
import sys

from bobotinho.config import config_dict
from bobotinho.logger import log

try:
    config_mode = os.getenv("CONFIG_MODE", "local")
    bot_config = config_dict[config_mode]
    log.info(f"Run with CONFIG_MODE={config_mode}")
except KeyError:
    sys.exit("[FATAL] Invalid <CONFIG_MODE>. Expected 'local', 'test' or 'prod'.")

loop = asyncio.get_event_loop()

try:
    from bobotinho.bot import Bobotinho
    bot = Bobotinho(bot_config, loop=loop)
except Exception as e:
    log.exception(e)
    sys.exit("[FATAL] Bot constructor failure")

try:
    from bobotinho.database import Database
    db = Database(bot_config.dbs_url)
except Exception as e:
    log.exception(e)
    sys.exit("[FATAL] Database constructor failure")

try:
    # TODO: forma provisória para adicionar novos canais (aka. gambiarra)
    from bobotinho.app import app
    app.secret_key = os.urandom(24)
except Exception as e:
    log.exception(e)
    sys.exit("[FATAL] App constructor failure")


def run():
    try:
        loop.run_until_complete(db.init())
        loop.run_until_complete(bot._ws._connect())
        loop.run_until_complete(db.register_init())
        loop.run_in_executor(None, app.run, "0.0.0.0", bot_config.port)
        loop.run_until_complete(bot._ws._listen())
    except BaseException as e:
        log.exception(e)
        loop.run_until_complete(db.register_close(e))
    else:
        loop.run_until_complete(db.register_close())
    finally:
        loop.run_until_complete(bot._ws._websocket.close())
        loop.run_until_complete(db.close())
