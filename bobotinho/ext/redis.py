# -*- coding: utf-8 -*-
from redis import Redis

from bobotinho.ext.config import config


redis = Redis.from_url(config.redis_url, encoding="utf-8", decode_responses=True)
