# -*- coding: utf-8 -*-
import random

from bobotinho.apis import Movie

description = "Recebe informações ou sugestões de filme, e até onde assistí-lo"
usage = "digite o comando e alguma tag: top, trend, popular, ou o nome de um filme"


async def command(ctx, arg: str, *, content: str = ""):
    arg = arg.lower()
    if arg in ("now", "upcoming", "latest", "popular", "top", "trend"):
        movie = await getattr(Movie, arg)()
    elif arg == "discover":
        provider = Movie.main_providers.get(content.lower())
        movie = await Movie.discover(provider)
    elif arg in ("similar", "recommendation"):
        movie = await Movie.find(content)
        if movie.get("id"):
            movie = await getattr(Movie, arg)(movie["id"])
        else:
            movie = {}
    else:
        content = f"{arg} {content}"
        movie = await Movie.find(content)
        movie.pop("genre_ids", None)

    if movie.get("results"):
        movie = random.sample(movie["results"], 1)[0]

    if movie.get("id"):
        id = movie["id"]
        title = movie["title"]
        year = movie["release_date"][:4]

        try:
            genre_id = movie["genre_ids"][0]
            quote = Movie.genre_id_to_quote[genre_id]
        except KeyError:
            quote = None

        try:
            watch = await Movie.watch(id)
            providers = ", ".join([p["provider_name"] for p in watch["results"]["BR"]["flatrate"]])
        except KeyError:
            providers = None

        if quote:
            ctx.response = f"{quote} {title} ({year})"
        else:
            ctx.response = f"veja o filme: {title} ({year})"
        if providers:
            ctx.response += f", disponível em {providers}"
    else:
        ctx.response = "não encontrei... se não estiver conseguindo, tente me enviar o link do IMDb"
