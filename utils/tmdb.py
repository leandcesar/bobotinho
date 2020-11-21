# -*- coding: utf-8 -*-

"""
Adapted from: https://github.com/celiao/tmdbsimple/tree/fa59c35a8f39dba37872c03d00840b7befe691cf
"""

import json
import re
import config

from difflib import SequenceMatcher
from itertools import filterfalse
from operator import itemgetter
from typing import Union
from unidecode import unidecode
from utils import asyncrq


status = {
    "Canceled": "Cancelado", 
    "Ended": "Encerrado", 
    "In Production": "Em produção", 
    "Post Production": "Em pós-produção",
    "Released": "Lançado",
    "Returning Series": "Retornará", 
    "Rumored": "Rumor", "Planned": "Em planejamento",
}


genres = {
    12: "Aventura", 14: "Fantasia", 16: "Animação", 18: "Drama", 27: "Terror", 
    28: "Ação", 35: "Comédia", 36: "História", 37: "Faroeste", 80: "Crime", 
    99: "Documentário", 878: "Ficção científica", 53: "Thriller", 9648: "Mistério", 
    10402: "Música", 10749: "Romance", 10751: "Família", 10752: "Guerra", 
    10759: "Ação e Aventura", 10763: "Jornalístico", 10762: "Infantil", 
    10764: "Reality show", 10765: "Ficção científica e Fantasia", 10766: "Soap opera", 
    10767: "Talk show", 10768: "Guerra e Política", 10770: "Cinema TV",
}


# Not implemented: freebase_mid, freebase_id, tvrage_id
url_external_ids = {
    "facebook_id": "https://www.facebook.com",
    "imdb_id": "https://www.imdb.comname",
    "instagram_id": "https://www.instagram.com",
    "twitter_id": "https://www.twitter.com",
}


def _sort_by_similarity(results: list, query: str):
    """
        Sort the list of search results (of movies, tv shows
        and persons) by similarity with the searched query.
    """
    query = unidecode(query).lower()

    def sequence_matcher(a: str, b: str):
        seq = SequenceMatcher(None, a, b)
        match = seq.find_longest_match(0, len(a), 0, len(b))
        return (seq.ratio(), match.size)

    def two_sequences_matcher(r: dict, key1: str, key2: str):
        ratio1, match1 = sequence_matcher(query, unidecode(r[key1]).lower())
        ratio2, match2 = sequence_matcher(query, unidecode(r[key2]).lower())
        if match1 == match2:
            return (ratio1, match1) if ratio1 >= ratio2 else (ratio2, match2)
        else:
            return (ratio1, match1) if match1 >= match2 else (ratio2, match2)

    similarity = []
    for r in results:
        if hasattr(r, "original_title"):
            ratio, match = two_sequences_matcher(r, getattr(r, "title"), getattr(r, "original_title"))
        elif hasattr(r, "original_name"):
            ratio, match = two_sequences_matcher(r, getattr(r, "name"), getattr(r, "original_name"))
        elif hasattr(r, "name"):
            ratio, match = sequence_matcher(query, unidecode(r["name"]).lower())
        else:
            continue
        similarity.append((match, getattr(r, "popularity", 0), ratio, r))
    
    sorted_results = [r[3] for r in sorted(similarity, key=itemgetter(0, 1, 2), reverse=True)]
    return sorted_results


def _obj_to_str(obj: Union[list, dict], attr: str, **kwargs):
    """
        Converts a list of dicts or a dict to str based on a attr, e.g.:
            Arguments:
                obj = [{"a": 0, "b": True}, {"a": 1, "b": False}, {"a": 2, "b": True}]
                attr = "a"
                expression = {"key": "b", "value": True}
            Returns:
                "0, 2"
    """
    if not obj or not attr:
        return None
    elif isinstance(obj, dict):
        return obj.get(attr, None)
    elif isinstance(obj, list):
        pass
    else:
        return None

    expression = kwargs.get("expression", None)
    lenght = kwargs.get("lenght", None)
    
    if expression and isinstance(expression, dict):
        if expression.get("key", None) and expression.get("value", None):
            key = str(expression["key"])
            value = expression["value"]
            obj = list(filterfalse(lambda x: x.get(key, None) != value, obj))
    if lenght and isinstance(lenght, int):
        return ", ".join(x[attr] for x in obj[:lenght])
    return ", ".join(x[attr] for x in obj)


def _id_to_hyperlink(external_ids: str, external_id: str):
    """
        Converts an external ID to hyperlinked str.
    """
    if not external_ids.get(external_id, None):
        return
    url = url_external_ids.get(external_id, None)
    if not url:
        return
    return "[@{id}]({url}/{id})".format(url=url, id=external_ids[external_id])


class APIKeyError(Exception):
    pass


class TMDB(object):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Connection": "close",
    }
    BASE_PATH = ""
    URLS = {}

    def __init__(self):
        self.base_uri = "https://api.themoviedb.org/{version}".format(version=3)

    def _get_path(self, key):
        return self.BASE_PATH + self.URLS[key]

    def _get_id_path(self, key):
        return self._get_path(key).format(id=getattr(self, "id"))

    def _get_credit_id_path(self, key):
        return self._get_path(key).format(credit_id=getattr(self, "credit_id"))

    def _get_media_type_time_window_path(self, key):
        return self._get_path(key).format(
            media_type=getattr(self, "media_type"),
            time_window=getattr(self, "time_window"),
        )

    def _get_tv_id_season_number_path(self, key):
        return self._get_path(key).format(
            tv_id=getattr(self, "tv_id"),
            season_number=getattr(self, "season_number")
        )

    def _get_tv_id_season_number_episode_number_path(self, key):
        return self._get_path(key).format(
            tv_id=getattr(self, "tv_id"),
            season_number=getattr(self, "season_number"),
            episode_number=getattr(self, "episode_number"),
        )

    def _get_complete_url(self, path):
        return "{base_uri}/{path}".format(base_uri=self.base_uri, path=path)

    def _get_params(self, params):
        if not config.Vars.apikey_tmdb:
            raise APIKeyError
        api_dict = {"api_key": config.Vars.apikey_tmdb}
        if params:
            params.update(api_dict)
            for key, value in params.items():
                if isinstance(params[key], bool):
                    params[key] = "true" if value is True else "false"
        else:
            params = api_dict
        return params

    async def _request(self, method, path, params=None, payload=None):
        url = self._get_complete_url(path)
        params = self._get_params(params)
        response = await asyncrq.get(
            url,
            params=params,
            data=json.dumps(payload) if payload else payload,
            headers=self.headers,
            res_method="json",
            no_cache=True,
        )
        return response

    async def _GET(self, path, params=None):
        return await self._request("GET", path, params=params)

    async def _GET_and_set_attrs_to_values(self, path, **kwargs):
        response = await self._GET(path, kwargs)
        if isinstance(response, dict):
            for key in response.keys():
                if not hasattr(self, key) or not callable(getattr(self, key)):
                    setattr(self, key, response[key])
        return response


class Movie(TMDB):
    """
        Not implemented (because I was not interested in using it):
            account_states, alternative_titles, changes, 
            release_dates, translations, reviews, latest.
    """

    BASE_PATH = "movie"
    URLS = {
        "details": "/{id}",                         # supports language
        "credits": "/{id}/credits",
        "external_ids": "/{id}/external_ids",
        "images": "/{id}/images",                   # supports language
        "keywords": "/{id}/keywords",
        "videos": "/{id}/videos",
        "recommendations": "/{id}/recommendations", # supports language
        "similar_movies": "/{id}/similar_movies",   # supports language
        "lists": "/{id}/lists",                     # supports language
        "now_playing": "/now_playing",              # supports language
        "popular": "/popular",                      # supports language
        "top_rated": "/top_rated",                  # supports language
        "upcoming": "/upcoming",                    # supports language
        "releases": "/{id}/releases",               # backward compatability
    }

    def __init__(self, id=0):
        super(Movie, self).__init__()
        self.id = id

    async def details(self, **kwargs):
        # See: https://developers.themoviedb.org/3/movies/get-movie-details
        return await self._GET_and_set_attrs_to_values(self._get_id_path("details"), **kwargs)

    async def defcredits(self, **kwargs):
        # See: https://developers.themoviedb.org/3/movies/get-movie-credits
        return await self._GET_and_set_attrs_to_values(self._get_id_path("credits"), **kwargs)

    async def def_ids(self, **kwargs): 
        # https://developers.themoviedb.org/3/movies/get-movie-external-ids
        return await self._GET_and_set_attrs_to_values(self._get_id_path("external_ids"), **kwargs)

    async def images(self, **kwargs):
        # See: https://developers.themoviedb.org/3/movies/get-movie-images
        return await self._GET_and_set_attrs_to_values(self._get_id_path("images"), **kwargs)

    async def keywords(self):
        # See: https://developers.themoviedb.org/3/movies/get-movie-keywords
        return await self._GET_and_set_attrs_to_values(self._get_id_path("keywords"))

    async def videos(self, **kwargs):
        # See: https://developers.themoviedb.org/3/movies/get-movie-videos
        return await self._GET_and_set_attrs_to_values(self._get_id_path("videos"), **kwargs)

    async def lists(self, **kwargs):
        # See: https://developers.themoviedb.org/3/movies/get-movie-lists
        return await self._GET_and_set_attrs_to_values(self._get_id_path("lists"), **kwargs)

    async def recommendations(self, **kwargs):
        # See: https://developers.themoviedb.org/3/movies/get-movie-recommendations
        return await self._GET_and_set_attrs_to_values(self._get_id_path("recommendations"), **kwargs)

    async def similar_movies(self, **kwargs):
        # See: https://developers.themoviedb.org/3/movies/get-movie-similar-movies
        return await self._GET_and_set_attrs_to_values(self._get_id_path("similar_movies"), **kwargs)

    async def now_playing(self, **kwargs):
        # See: https://developers.themoviedb.org/3/movies/get-movie-now-playing
        return await self._GET_and_set_attrs_to_values(self._get_path("now_playing"), **kwargs)

    async def popular(self, **kwargs):
        # See: https://developers.themoviedb.org/3/movies/get-movie-popular
        return await self._GET_and_set_attrs_to_values(self._get_path("popular"), **kwargs)

    async def releases(self, **kwargs):
        # See: https://developers.themoviedb.org/3/movies/get-movie-releases
        return await self._GET_and_set_attrs_to_values(self._get_path("releases"), **kwargs)

    async def top_rated(self, **kwargs):
        # See: https://developers.themoviedb.org/3/movies/get-movie-top-rated
        return await self._GET_and_set_attrs_to_values(self._get_path("top_rated"), **kwargs)

    async def upcoming(self, **kwargs):
        # See: https://developers.themoviedb.org/3/movies/get-movie-upcoming
        return await self._GET_and_set_attrs_to_values(self._get_path("upcoming"), **kwargs)

    
class Collection(TMDB):
    """
        Not implemented (because I was not interested in using it):
            translations.
    """

    BASE_PATH = "collection"
    URLS = {
        "details": "/{id}",         # supports language
        "images": "/{id}/images",   # supports language
    }

    def __init__(self, id):
        super(Collection, self).__init__()
        self.id = id

    async def details(self, **kwargs):
        # See: https://developers.themoviedb.org/3/collections/get-collection-details
        return await self._GET_and_set_attrs_to_values(self._get_id_path("details"), **kwargs)

    async def images(self, **kwargs):
        # See: https://developers.themoviedb.org/3/collections/get-collection-images
        return await self._GET_and_set_attrs_to_values(self._get_id_path("images"), **kwargs)


class Keyword(TMDB):
    """
        Not implemented (because I was not interested in using it):
            translations.
    """

    BASE_PATH = "keyword"
    URLS = {
        "details": "/{id}",
        "movies": "/{id}/movies",  # supports language
    }

    def __init__(self, id):
        super(Keyword, self).__init__()
        self.id = id

    async def details(self, **kwargs):
        # See: https://developers.themoviedb.org/3/keywords/get-keyword-details
        return await self._GET_and_set_attrs_to_values(self._get_id_path("details"), **kwargs)

    async def movies(self, **kwargs):
        # See: https://developers.themoviedb.org/3/keywords/get-keyword-movies
        return await self._GET_and_set_attrs_to_values(self._get_id_path("movies"), **kwargs)


class Person(TMDB):
    """
        Not implemented (because I was not interested in using it):
            changes, translations, latest
    """
    
    BASE_PATH = "person"
    URLS = {
        "details": "/{id}",
        "movie_credits": "/{id}/movie_credits",         # supports language
        "tv_credits": "/{id}/tv_credits",               # supports language
        "combined_credits": "/{id}/combined_credits",   # supports language
        "external_ids": "/{id}/external_ids",
        "images": "/{id}/images",
        "tagged_images": "/{id}/tagged_images",
        "popular": "/popular",
    }

    def __init__(self, id=0):
        super(Person, self).__init__()
        self.id = id

    async def details(self, **kwargs):
        # See: https://developers.themoviedb.org/3/people/get-person-details
        return await self._GET_and_set_attrs_to_values(self._get_id_path("details"), **kwargs)

    async def movie_credits(self, **kwargs):
        # See: https://developers.themoviedb.org/3/people/get-person-movie-credits
        return await self._GET_and_set_attrs_to_values(self._get_id_path("movie_credits"), **kwargs)

    async def tv_credits(self, **kwargs):
        # See: https://developers.themoviedb.org/3/people/get-person-tv-credits
        return await self._GET_and_set_attrs_to_values(self._get_id_path("tv_credits"), **kwargs)

    async def def_credits(self, **kwargs):
        # See: https://developers.themoviedb.org/3/people/get-person-combined-credits
        return await self._GET_and_set_attrs_to_values(self._get_id_path("combined_credits"), **kwargs)

    async def def_ids(self, **kwargs):
        # See: https://developers.themoviedb.org/3/people/get-person-external-ids
        return await self._GET_and_set_attrs_to_values(self._get_id_path("external_ids"), **kwargs)

    async def images(self, **kwargs):
        # See: https://developers.themoviedb.org/3/people/get-person-images
        return await self._GET_and_set_attrs_to_values(self._get_id_path("images"), **kwargs)

    async def tagged_images(self, **kwargs):
        # See: https://developers.themoviedb.org/3/people/get-person-tagged-images
        return await self._GET_and_set_attrs_to_values(self._get_id_path("tagged_images"), **kwargs)

    async def popular(self, **kwargs):
        # See: https://developers.themoviedb.org/3/people/get-person-popular
        return await self._GET_and_set_attrs_to_values(self._get_path("popular"), **kwargs)


class Credits(TMDB):

    BASE_PATH = "credit"
    URLS = {
        "details": "/{credit_id}",  # supports language
    }

    def __init__(self, credit_id):
        super(Credits, self).__init__()
        self.credit_id = credit_id

    async def details(self, **kwargs):
        # See: https://developers.themoviedb.org/3/credits/get-credit-details
        return await self._GET_and_set_attrs_to_values(self._get_credit_id_path("details"), **kwargs)


class Discover(TMDB):

    BASE_PATH = "discover"
    URLS = {
        "movie": "/movie",
        "tv": "/tv",
    }

    async def movie(self, **kwargs):
        """
            See: https://developers.themoviedb.org/3/discover/movie-discover

            Arguments:
                language...................str
                region.....................str
                sort_by....................str
                    Allowed Values:
                        popularity.asc, popularity.desc, release_date.asc, 
                        release_date.desc, revenue.asc, revenue.desc, 
                        primary_release_date.asc, primary_release_date.desc, 
                        original_title.asc, original_title.desc, vote_average.asc, 
                        vote_average.desc, vote_count.asc, vote_count.desc
                certification_country......str
                certification..............str
                certification.lte..........str
                certification.gte..........str
                include_adult..............bool
                include_video..............bool
                primary_release_year.......int
                primary_release_date.gte...str
                primary_release_date.lte...str
                release_date.gte...........str
                release_date.lte...........str
                with_release_type..........int
                year.......................int
                vote_count.gte.............int
                vote_count.lte.............int
                vote_average.gte...........float
                vote_average.lte...........float
                with_cast..................str
                with_crew..................str
                with_people................str
                with_companies.............str
                with_genres................str
                without_genres.............str
                with_keywords..............str
                without_keywords...........str
                with_runtime.gte...........int
                with_runtime.lte...........int
                with_original_language.....str
        """
        return await self._GET_and_set_attrs_to_values(self._get_path("movie"), **kwargs)

    async def tv(self, **kwargs):
        """
            See: https://developers.themoviedb.org/3/discover/tv-discover

            Arguments:
                language...................str
                region.....................str
                sort_by....................str
                    Allowed Values:
                        vote_average.desc, vote_average.asc, first_air_date.desc, 
                        first_air_date.asc, popularity.desc, popularity.asc
                air_date.gte...............str
                air_date.lte...............str
                first_air_date.gte.........str
                first_air_date.lte.........str
                first_air_date_year........str
                timezone...................str
                vote_average.gte...........float
                vote_count.gte.............int
                with_genres................str
                with_runtime.gte...........int
                with_runtime.lte...........int
                with_original_language.....str
                without_keywords...........str
                with_companies.............str
                with_keywords..............str
        """
        return await self._GET_and_set_attrs_to_values(self._get_path("tv"), **kwargs)


class Find(TMDB):

    BASE_PATH = "find"
    URLS = {
        "details": "/{id}",
    }

    def __init__(self, id=0):
        super(Find, self).__init__()
        self.id = id

    async def details(self, **kwargs):
        """
            See: https://developers.themoviedb.org/3/find/find-by-id
        """
        return await self._GET_and_set_attrs_to_values(self._get_id_path("details"), **kwargs)


class Search(TMDB):

    BASE_PATH = "search"
    URLS = {
        "company": "/company",
        "collection": "/collection",    # supports language
        "keyword": "/keyword",
        "movie": "/movie",              # supports language, include_adult
        "multi": "/multi",              # supports language, include_adult
        "person": "/person",            # supports include_adult
        "tv": "/tv",                    # supports language, include_adult
    }

    async def company(self, **kwargs):
        # See: https://developers.themoviedb.org/3/search/search-companies
        return await self._GET_and_set_attrs_to_values(self._get_path("company"), **kwargs)

    async def collection(self, **kwargs):
        # See: https://developers.themoviedb.org/3/search/search-collections
        return await self._GET_and_set_attrs_to_values(self._get_path("collection"), **kwargs)

    async def keyword(self, **kwargs):
        # See: https://developers.themoviedb.org/3/search/search-keywords
        return await self._GET_and_set_attrs_to_values(self._get_path("keyword"), **kwargs)

    async def movie(self, **kwargs):
        # See: https://developers.themoviedb.org/3/search/search-movies
        return await self._GET_and_set_attrs_to_values(self._get_path("movie"), **kwargs)

    async def multi(self, **kwargs):
        # See: https://developers.themoviedb.org/3/search/multi-search
        return await self._GET_and_set_attrs_to_values(self._get_path("multi"), **kwargs)

    async def person(self, **kwargs):
        # See: https://developers.themoviedb.org/3/search/search-people
        return await self._GET_and_set_attrs_to_values(self._get_path("person"), **kwargs)

    async def tv(self, **kwargs):
        # See: https://developers.themoviedb.org/3/search/search-tv-shows
        return await self._GET_and_set_attrs_to_values(self._get_path("tv"), **kwargs)
   

class Trending(TMDB):

    BASE_PATH = "trending"
    URLS = {
        "details": "/{media_type}/{time_window}",
    }

    def __init__(self, media_type="all", time_window="day"):
        super(Trending, self).__init__()
        self.media_type = media_type
        self.time_window = time_window

    async def details(self, **kwargs):
        """
            See: https://developers.themoviedb.org/3/trending/get-trending
        """
        return await self._GET_and_set_attrs_to_values(self._get_media_type_time_window_path("details"), **kwargs)


class TV(TMDB):
    """
        Not implemented (because I was not interested in using it):
            alternative_names.
    """
    
    BASE_PATH = "tv"
    URLS = {
        "details": "/{id}",                         # supports language
        "content_ratings": "/{id}/content_ratings", # supports language
        "credits": "/{id}/credits",                 # supports language
        "episode_groups": "/{id}/episode_groups",   # supports language
        "external_ids": "/{id}/external_ids",       # supports language
        "images": "/{id}/images",                   # supports language
        "keywords": "/{id}/keywords",
        "recommendations": "/{id}/recommendations", # supports language
        "similar": "/{id}/similar",                 # supports language
        "videos": "/{id}/videos",                   # supports language
        "airing_today": "/airing_today",            # supports language, timezone
        "on_the_air": "/on_the_air",                # supports language
        "popular": "/popular",                      # supports language
        "top_rated": "/top_rated",                  # supports language
    }

    def __init__(self, id=0):
        super(TV, self).__init__()
        self.id = id

    async def details(self, **kwargs):
        # https://developers.themoviedb.org/3/tv/get-tv-details
        return await self._GET_and_set_attrs_to_values(self._get_id_path("details"), **kwargs)

    async def content_ratings(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv/get-tv-content-ratings
        return await self._GET_and_set_attrs_to_values(self._get_id_path("content_ratings"), **kwargs)

    async def defcredits(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv/get-tv-credits
        return await self._GET_and_set_attrs_to_values(self._get_id_path("credits"), **kwargs)

    async def episode_groups(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv/get-tv-episode-groups
        return await self._GET_and_set_attrs_to_values(self._get_id_path("episode_groups"), **kwargs)

    async def def_ids(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv/get-tv-external-ids
        return await self._GET_and_set_attrs_to_values(self._get_id_path("external_ids"), **kwargs)

    async def images(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv/get-tv-images
        return await self._GET_and_set_attrs_to_values(self._get_id_path("images"), **kwargs)

    async def keywords(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv/get-tv-keywords
        return await self._GET_and_set_attrs_to_values(self._get_id_path("keywords"), **kwargs)

    async def recommendations(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv/get-tv-recommendations
        return await self._GET_and_set_attrs_to_values(self._get_id_path("recommendations"), **kwargs)

    async def similar(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv/get-tv-similar
        return await self._GET_and_set_attrs_to_values(self._get_id_path("similar"), **kwargs)

    async def videos(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv/get-tv-videos
        return await self._GET_and_set_attrs_to_values(self._get_id_path("videos"), **kwargs)
       
    async def airing_today(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv/get-tv-airing-today
        return await self._GET_and_set_attrs_to_values(self._get_path("airing_today"), **kwargs)

    async def on_the_air(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv/get-tv-on-the-air
        return await self._GET_and_set_attrs_to_values(self._get_path("on_the_air"), **kwargs)

    async def popular(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv/get-tv-popular
        return await self._GET_and_set_attrs_to_values(self._get_path("popular"), **kwargs)

    async def top_rated(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv/get-tv-top-rated
        return await self._GET_and_set_attrs_to_values(self._get_path("top_rated"), **kwargs)

    
class TV_Seasons(TMDB):
    """
        Not implemented (because I was not interested in using it):
            account_states.
    """

    BASE_PATH = "tv/{tv_id}/season/{season_number}"
    URLS = {
        "details": "",                      # supports language
        "credits": "/credits",
        "external_ids": "/external_ids",    # supports language
        "images": "/images",                # supports language
        "videos": "/videos",                # supports language
    }

    def __init__(self, tv_id, season_number):
        super(TV_Seasons, self).__init__()
        self.tv_id = tv_id
        self.season_number = season_number

    async def details(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv-seasons/get-tv-season-details
        return await self._GET_and_set_attrs_to_values(self._get_tv_id_season_number_path("details"), **kwargs)

    async def defcredits(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv-seasons/get-tv-season-credits
        return await self._GET_and_set_attrs_to_values(self._get_tv_id_season_number_path("credits"), **kwargs)

    async def def_ids(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv-seasons/get-tv-season-external-ids
        return await self._GET_and_set_attrs_to_values(self._get_tv_id_season_number_path("external_ids"), **kwargs)

    async def images(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv-seasons/get-tv-season-images
        return await self._GET_and_set_attrs_to_values(self._get_tv_id_season_number_path("images"), **kwargs)

    async def videos(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv-seasons/get-tv-season-videos
        return await self._GET_and_set_attrs_to_values(self._get_tv_id_season_number_path("videos"), **kwargs)
        

class TV_Episodes(TMDB):
    """
        Not implemented (because I was not interested in using it):
            account_states, rating.
    """

    BASE_PATH = "tv/{tv_id}/season/{season_number}/episode/{episode_number}"
    URLS = {
        "details": "",                      # supports language
        "credits": "/credits",
        "external_ids": "/external_ids",
        "images": "/images",                # supports language
        "videos": "/videos",                # supports language
    }

    def __init__(self, tv_id, season_number, episode_number):
        super(TV_Episodes, self).__init__()
        self.tv_id = tv_id
        self.season_number = season_number
        self.episode_number = episode_number

    async def details(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv-episodes/get-tv-episode-details
        return await self._GET_and_set_attrs_to_values(self._get_tv_id_season_number_episode_number_path("details"), **kwargs)

    async def defcredits(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv-episodes/get-tv-episode-credits
        return await self._GET_and_set_attrs_to_values(self._get_tv_id_season_number_episode_number_path("credits"), **kwargs)

    async def def_ids(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv-episodes/get-tv-episode-external-ids
        return await self._GET_and_set_attrs_to_values(self._get_tv_id_season_number_episode_number_path("external_ids"), **kwargs)

    async def images(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv-episodes/get-tv-episode-images
        return await self._GET_and_set_attrs_to_values(self._get_tv_id_season_number_episode_number_path("images"), **kwargs)

    async def videos(self, **kwargs): 
        # https://developers.themoviedb.org/3/tv-episodes/get-tv-episode-videos
        return await self._GET_and_set_attrs_to_values(self._get_tv_id_season_number_episode_number_path("videos"), **kwargs)
