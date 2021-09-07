# -*- coding: utf-8 -*-
from bobotinho.apis import Weather

description = "Saiba o clima atual de alguma cidade"
aliases = ["wt"]
usage = "digite o comando e o nome de um local para saber o clima"


async def command(ctx, *, content: str = None):
    if not content:
        place = ctx.user.city
    else:
        place = content
    if place in ("salvador", "socorro", "santiago"):
        place = f"{place}, br"
    try:
        observation = Weather.weather_at_place(place)
        city = observation.location.name
        country = observation.location.country
        status = observation.weather.detailed_status
        temperature = observation.weather.temperature("celsius")
        temp = temperature["temp"]
        feels_like = temperature["feels_like"]
        wind = observation.weather.wind()["speed"]
        humidiy = observation.weather.humidity
        ctx.response = (
            f"em {city} ({country}): {status}, {temp}°C (sensação de "
            f"{feels_like}°C), ventos a {wind}m/s e {humidiy}% de umidade"
        )
    except AssertionError:
        ctx.response = "digite o comando e o nome de um local para saber o clima"
    except Exception:
        ctx.response = "não há nenhuma previsão para esse local"
