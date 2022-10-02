# -*- coding: utf-8 -*-
from bobotinho.bot import Bobotinho
from bobotinho.ext.config import config

try:
    bot = Bobotinho(
        token=config.token,
        client_secret=config.secret,
        prefix=config.prefix,
        initial_channels=[config.dev],
        case_insensitive=True,
    )
    bot.load_modules(cogs=[f"{config.cogs_path}.{cog}" for cog in config.cogs])
    bot.start()
except KeyboardInterrupt:
    pass
finally:
    bot.stop()
