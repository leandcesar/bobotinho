# -*- coding: utf-8 -*-
import random
import re

from bobotinho.apis import Discover, Find, Movie, Trending

description = "Receba informações ou sugestões de filme, e até onde assistí-lo"
usage = "digite o comando e alguma tag: top, trend, popular, ou o nome de um filme"

METHODS = {
    "now": Movie.now_playing,
    "upcoming": Movie.upcoming,
    "popular": Movie.popular,
    "top": Movie.top_rated,
    "trend": Trending.movie_week,
}

PROVIDERS = {
    "netflix": 8,
    "prime": 119,
    "disney+": 337,
    "itunes": 2,
    "google": 3,
    "looke": 47,
    "fox": 229,
    "mubi": 11,
    "star+": 619,
    "paramount+": 531,
    "hbo": 384,
    "claro": 167,
    "telecine": 227,
    "globo": 307,
}


def find_movie(query: str):
    if not query:
        return None
    try:
        imdb_id = re.search(r"(?:imdb.com\/title\/)?(tt[0-9]{7})", query)[1]
    except TypeError:
        movie = Movie.search(query)[0]
    else:
        movie = Find.find_by_imdb_id(imdb_id)["movie_results"][0]
    finally:
        return movie


def discover_movie(provider: str):
    try:
        movies = Discover.movies({"with_watch_providers": PROVIDERS[provider]})
    except KeyError:
        movies = Discover.movies({})
    finally:
        return movies


async def command(ctx, arg: str, *, content: str = ""):
    arg = arg.lower()
    content = content.lower()
    if not content and arg in METHODS:
        movies = METHODS[arg]()
    elif arg == "discover":
        movies = discover_movie(content)
    elif arg == "similar":
        movie = find_movie(content)
        movies = Movie.similar(movie.id) if movie else []
    elif arg == "recommendation":
        movie = find_movie(content)
        movies = Movie.recommendations(movie.id) if movie else []
    else:
        movies = find_movie(f"{arg} {content}")

    try:
        movie = random.sample(movies, 1)[0] if isinstance(movies, list) else movies
        movie_id = movie["id"]
        title = movie["title"]
        year = movie["release_date"][:4]
        providers = Movie.providers(movie_id)
        ctx.response = f"veja o filme: {title} ({year})"
        try:
            providers_br = providers["results"]["BR"]["flatrate"]
            providers_br = ", ".join([provider["provider_name"] for provider in providers_br])
            ctx.response += f", disponível em {providers_br}"
        except KeyError:
            pass
    except Exception:
        ctx.response = "não encontrei o filme... confira se escreveu corretamente ou me envie o link do IMDb"
