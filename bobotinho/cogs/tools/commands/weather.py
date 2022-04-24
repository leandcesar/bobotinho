# -*- coding: utf-8 -*-
description = "Saiba o clima atual de alguma cidade"
aliases = ["wt"]
usage = "digite o comando e o nome de um local para saber o clima"


async def command(ctx, *, content: str = ""):
    place = content or ctx.user.city
    if place in ("salvador", "socorro", "santiago"):
        place = f"{place}, br"
    if place:
        try:
            weather = await ctx.bot.api.weather(place)
            city = weather["name"]
            country = weather["country"]
            status = weather["description"]
            temperature = weather["temp"]
            feels_like = weather["temp_feels_like"]
            wind = weather["speed"]
            humidiy = weather["humidity"]
            emoji = weather["emoji"]
            ctx.response = (
                f"em {city} ({country}): {status} {emoji}, {temperature}°C (sensação de "
                f"{feels_like}°C), ventos a {wind}m/s e {humidiy}% de umidade"
            )
        except Exception:
            ctx.response = "não há nenhuma previsão para esse local"
    else:
        ctx.response = "digite o comando e o nome de um local para saber o clima"
