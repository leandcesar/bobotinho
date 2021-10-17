# -*- coding: utf-8 -*-
import random
import re

from bobotinho.apis import Discover, Find, Trending, TV

description = "Receba informações ou sugestões de uma série, e até onde assistí-la"
usage = "digite o comando e alguma tag: top, trend, popular, ou o nome de uma série"

METHODS = {
    "now": TV.on_the_air,
    "popular": TV.popular,
    "top": TV.top_rated,
    "trend": Trending.tv_week,
}

PROVIDERS = {
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


def find_tv_show(query: str):
    if not query:
        return None
    try:
        imdb_id = re.search(r"(?:imdb.com\/title\/)?(tt[0-9]{7})", query)[1]
    except TypeError:
        tv_show = TV.search(query)[0]
    else:
        tv_show = Find.find_by_imdb_id(imdb_id)["tv_results"][0]
    finally:
        return tv_show


def discover_tv_show(provider: str):
    try:
        tv_shows = Discover.tv_shows({"with_watch_providers": PROVIDERS[provider]})
    except KeyError:
        tv_shows = Discover.tv_shows({})
    finally:
        return tv_shows


async def command(ctx, arg: str, *, content: str = ""):
    arg = arg.lower()
    content = content.lower()
    if not content and arg in METHODS:
        tv_shows = METHODS[arg]()
    elif arg == "discover":
        tv_shows = discover_tv_show(content)
    elif arg == "similar":
        tv_show = find_tv_show(content)
        tv_shows = TV.similar(tv_show.id) if tv_show else []
    elif arg == "recommendation":
        tv_show = find_tv_show(content)
        tv_shows = TV.recommendations(tv_show.id) if tv_show else []
    else:
        tv_shows = find_tv_show(f"{arg} {content}")

    try:
        print(tv_shows)
        tv_show = random.sample(tv_shows, 1)[0] if isinstance(tv_shows, list) else tv_shows
        print(tv_show)
        tv_show_id = tv_show["id"]
        title = tv_show["name"]
        year = tv_show["first_air_date"][:4]
        providers = TV.providers(tv_show_id)
        ctx.response = f"veja a série: {title} ({year})"
        try:
            providers_br = providers["results"]["BR"]["flatrate"]
            providers_br = ", ".join([provider["provider_name"] for provider in providers_br])
            ctx.response += f", disponível em {providers_br}"
        except KeyError:
            pass
    except Exception:
        ctx.response = "não encontrei a série... confira se escreveu corretamente ou me envie o link do IMDb"
