# -*- coding: utf-8 -*-
import random

from bobotinho.apis import Tv

description = "Receba informações ou sugestões de uma série, e até onde assistí-la"
usage = "digite o comando e alguma tag: top, trend, popular, ou o nome de uma série"


async def command(ctx, arg: str, *, content: str = ""):
    arg = arg.lower()
    if arg in ("now", "latest", "popular", "top", "trend"):
        tv = await getattr(Tv, arg)()
    elif arg == "discover":
        provider = Tv.main_providers.get(content.lower())
        tv = await Tv.discover(provider)
    elif arg in ("similar", "recommendation"):
        tv = await Tv.find(content)
        if tv.get("id"):
            tv = await getattr(Tv, arg)(tv["id"])
        else:
            tv = {}
    else:
        content = f"{arg} {content}"
        tv = await Tv.find(content)
        tv.pop("genre_ids", None)

    if tv.get("results"):
        tv = random.sample(tv["results"], 1)[0]

    if tv.get("id"):
        id = tv["id"]
        title = tv["name"]
        year = tv["first_air_date"][:4]

        try:
            genre_id = tv["genre_ids"][0]
            quote = Tv.genre_id_to_quote[genre_id]
        except KeyError:
            quote = None

        try:
            watch = await Tv.watch(id)
            providers = ", ".join([p["provider_name"] for p in watch["results"]["BR"]["flatrate"]])
        except KeyError:
            providers = None

        if quote:
            ctx.response = f"{quote} {title} ({year})"
        else:
            ctx.response = f"veja a série: {title} ({year})"
        if providers:
            ctx.response += f", disponível em {providers}"
    else:
        ctx.response = "não encontrei... se não estiver conseguindo, tente me enviar o link do IMDb"
