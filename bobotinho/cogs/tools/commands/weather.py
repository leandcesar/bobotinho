# -*- coding: utf-8 -*-
from bobotinho.apis import Weather

description = "Saiba o clima atual de alguma cidade"
aliases = ["wt"]
usage = "digite o comando e o nome de um local para saber o clima"


async def command(ctx, *, content: str = ""):
    if not content:
        place = ctx.user.city
    else:
        place = content.lower()
    if place in ("salvador", "socorro", "santiago"):
        place = f"{place}, br"
    try:
        observation = Weather.weather_at_place(place)
        city = observation.get_location().get_name()
        country = observation.get_location().get_country()
        status = observation.get_weather().get_detailed_status()
        temp = observation.get_weather().get_temperature("celsius")["temp"]
        wind = observation.get_weather().get_wind()["speed"]
        humidiy = observation.get_weather().get_humidity()
        ctx.response = (
            f"em {city} ({country}): {status}, {temp}°C, "
            f"ventos a {wind}m/s e {humidiy}% de umidade"
        )
    except AssertionError:
        ctx.response = "digite o comando e o nome de um local para saber o clima"
    except Exception:
        ctx.response = "não há nenhuma previsão para esse local"
