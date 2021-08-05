# -*- coding: utf-8 -*-
import sys

from bobotinho import config, log

try:
    from bobotinho.database import Database

    db: Database = Database(config.database_url)
except Exception as e:
    log.critical(e, exc_info=1)
    sys.exit("[CRITICAL] Database constructor failure")

try:
    from bobotinho.bots import TwitchBot

    bot: TwitchBot = TwitchBot(config)
except Exception as e:
    log.critical(e, exc_info=1)
    sys.exit("[CRITICAL] Twitch Bot constructor failure")

try:
    from redis import Redis

    bot.cache = Redis.from_url(config.redis_url, encoding="utf-8", decode_responses=True)
except Exception as e:
    from bobotinho.cache import TTLOrderedDict

    log.warning(e)
    bot.cache = TTLOrderedDict()


if __name__ == "__main__":
    try:
        bot.loop.run_until_complete(db.init())
        bot.loop.run_until_complete(db.register_init())
        bot.loop.run_until_complete(bot.connect())
        bot.loop.run_until_complete(bot.join_all_channels())
        bot.loop.run_until_complete(bot.fetch_blocked())
        bot.add_checks()
        bot.load_cogs()
        bot.loop.run_forever()
    except KeyboardInterrupt:
        bot.loop.run_until_complete(db.register_close())
    except Exception as e:
        bot.loop.run_until_complete(db.register_close(e))
        log.exception(e)
    else:
        bot.loop.run_until_complete(db.register_close())
    finally:
        bot.loop.run_until_complete(db.close())
        bot.cache.close()
        bot.loop.run_until_complete(bot.close())
        bot.loop.close()
