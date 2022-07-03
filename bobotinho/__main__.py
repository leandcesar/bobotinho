# -*- coding: utf-8 -*-
import asyncio

from bobotinho import config, database, log
from bobotinho.bot import Bobotinho
from bobotinho.cache import Cache
from bobotinho.database import Channel


async def get_channels():
    return await Channel.all().select_related("user")


def main():
    try:
        loop = asyncio.get_event_loop()
        cache = Cache(redis_url=config.redis_url)
        loop.run_until_complete(database.init(config.database_url))
        channels = loop.run_until_complete(get_channels())
        bot = Bobotinho(config, channels=channels, cache=cache)
    except Exception as e:
        log.critical(e, exc_info=1)
        cache.close()
        loop.run_until_complete(database.close())
        loop.close()
        exit("[CRITICAL] Bobotinho connection failure")

    try:
        loop.create_task(bot.connect())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        log.critical(e, exc_info=1)
    finally:
        loop.run_until_complete(bot.close())
        cache.close()
        loop.run_until_complete(database.close())
        loop.close()


if __name__ == "__main__":
    main()
