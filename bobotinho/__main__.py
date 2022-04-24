# -*- coding: utf-8 -*-
import sys

from bobotinho import config, log
from bobotinho.bot import TwitchBot


if __name__ == "__main__":
    try:
        bot = TwitchBot(config)
    except Exception as e:
        log.critical(e, exc_info=1)
        sys.exit("[CRITICAL] Twitch Bot constructor failure")

    try:
        bot.loop.run_until_complete(bot.start())
        bot.loop.run_forever()
    except KeyboardInterrupt:
        pass
    except BaseException as e:
        log.exception(e, extra={"locals": locals()})
    finally:
        bot.loop.run_until_complete(bot.stop())
        bot.loop.close()
