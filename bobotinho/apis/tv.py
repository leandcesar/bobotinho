# -*- coding: utf-8 -*-
import re
from aiocache import cached

from bobotinho import aiorequests, config


class Tv:
    base_url = config.tmdb_url
    key = config.tmdb_key
    genre_id_to_quote = {
        12: "que tal uma aventura?",
        14: "embarque em uma fantasia:",
        16: "quer uma bela animação?",
        18: "drama sempre cai bem:",
        27: "é hora do terror:",
        28: "experimente um pouco de ação:",
        35: "relaxe com uma boa comédia:",
        36: "você gosta de História?",
        37: "bang bang! Reviva o faroeste:",
        53: "reúna o pessoal pra esse suspense:",
        80: "embarque nesse crime:",
        99: "informe-se com esse documentário:",
        878: "que tal um pouco de ficção científica?",
        9648: "você gosta de um mistério?",
        10402: "solte a voz com esse musical:",
        10749: "mergulhe nesse romance:",
        10751: "reúna a família ou amigos e veja:",
        10752: "em clima de guerra:",
        10759: "um pouco de ação e aventura:",
        10763: "que tal experimentar algo jornalístico?",
        10762: "caso queira algo mais infantil:",
        10764: "por que não um reality show?",
        10765: "ficção científica e fantasia:",
        10766: "conhece o gênero soap opera?",
        10767: "por que não um talk show?",
        10768: "um pouco de guerra e política:",
        10770: "mergulhe no cinema:",
    }
    main_providers = {
        "netflix": 8,
        "prime": 119,
        "disney+": 337,
        "looke": 47,
        "fox": 229,
        "star+": 619,
        "paramount+": 531,
        "hbo": 384,
        "crunchyroll": 283,
        "claro": 167,
        "globo": 307,
    }

    @classmethod
    @cached(ttl=3600)
    async def request(cls, path, **kwargs):
        url = f"{cls.base_url}/{path}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Connection": "close",
        }
        default_params = {"api_key": cls.key, "language": "pt-BR"}
        params = kwargs.get("params")
        if params:
            params.update(default_params)
        else:
            params = default_params
        return await aiorequests.get(url, params=params, headers=headers)

    @classmethod
    async def details(cls, id):
        return await cls.request(f"tv/{id}")

    @classmethod
    async def credits(cls, id):
        return await cls.request(f"tv/{id}/credits")

    @classmethod
    async def ids(cls, id):
        return await cls.request(f"tv/{id}/external_ids")

    @classmethod
    async def ratings(cls):
        return await cls.request(f"tv/{id}/content_ratings")

    @classmethod
    async def episodes(cls, id):
        return await cls.request(f"tv/{id}/episode_groups")

    @classmethod
    async def recommendation(cls, id):
        return await cls.request(f"tv/{id}/recommendations")

    @classmethod
    async def similar(cls, id):
        return await cls.request(f"tv/{id}/similar")

    @classmethod
    async def watch(cls, id):
        return await cls.request(f"tv/{id}/watch/providers")

    @classmethod
    async def airing(cls):
        return await cls.request("tv/airing_today")

    @classmethod
    async def now(cls):
        return await cls.request("tv/on_the_air")

    @classmethod
    async def latest(cls):
        return await cls.request("tv/latest")

    @classmethod
    async def popular(cls):
        return await cls.request("tv/popular")

    @classmethod
    async def top(cls):
        return await cls.request("tv/top_rated")

    @classmethod
    async def discover(cls, provider):
        return await cls.request("discover/tv", params={"with_watch_providers": provider, "watch_region": "BR"})

    @classmethod
    async def trend(cls):
        return await cls.request("trending/tv/day")

    @classmethod
    async def search(cls, query):
        return await cls.request("search/tv", params={"query": query})

    @classmethod
    async def from_imdb(cls, imdb_id):
        return await cls.request(f"find/{imdb_id}", params={"external_source": "imdb_id"})

    @classmethod
    async def find(cls, query):
        imdb_id = re.search(r"(?:imdb.com\/title\/)?(tt[0-9]{9})", query)
        if imdb_id:
            return await cls.from_imdb(imdb_id[1])
        response = await cls.search(query)
        return response["results"][0] if response["results"] else {}
