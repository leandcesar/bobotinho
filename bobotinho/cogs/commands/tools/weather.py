# -*- coding: utf-8 -*-
from bobotinho.apis import weather

description = "Saiba o clima atual de alguma cidade"
aliases = ["wt"]
usage = "digite o comando e o nome de um local para saber o clima"


async def func(ctx, *, content: str):
    try:
        observation = weather.WeatherAPI.weather_at_place(content)
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
    except Exception:
        ctx.response = "não há nenhuma previsão para esse local"
