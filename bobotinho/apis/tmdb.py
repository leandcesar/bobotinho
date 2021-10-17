# -*- coding: utf-8 -*-
import os
import tmdb

from bobotinho import config, log

try:
    os.environ["TMDB_API_KEY"] = config.tmdb_key
    os.environ["TMDB_LANGUAGE"] = "pt-BR"
    os.environ["TMDB_REGION"] = "BR"
    Discover = tmdb.Discover()
    Genre = tmdb.Genre()
    Find = tmdb.Find()
    Movie = tmdb.Movie()
    Providers = tmdb.Providers()
    Trending = tmdb.Trending()
    TV = tmdb.TV()
except Exception as e:
    log.warning(e)
