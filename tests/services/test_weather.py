# -*- coding: utf-8 -*-
from unittest.mock import patch

import pytest
from bobotinho.services.weather import Weather


async def test_weather(mock_response):
    return_value = mock_response(
        data={
            "base": "stations",
            "clouds": {"all": 75},
            "cod": 200,
            "coord": {"lat": -22.9028, "lon": -43.2075},
            "dt": 1664325856,
            "id": 3451190,
            "main": {
                "feels_like": 23.72,
                "humidity": 82,
                "pressure": 1015,
                "temp": 23.2,
                "temp_max": 24,
                "temp_min": 21.12,
            },
            "name": "Rio de Janeiro",
            "sys": {"country": "BR", "id": 8429, "sunrise": 1664267844, "sunset": 1664311813, "type": 1},
            "timezone": -10800,
            "visibility": 10000,
            "weather": [{"description": "nublado", "icon": "04n", "id": 803, "main": "Clouds"}],
            "wind": {"deg": 250, "speed": 3.6},
        }
    )

    with patch("aiohttp.ClientSession.request", return_value=return_value) as mock_response:
        response = await Weather(key="s3cr3t").prediction(location="rio de janeiro")

    assert mock_response.call_count == 1
    assert mock_response.call_args[0] == ("get",)
    assert mock_response.call_args[1] == {
        "params": {
            "appid": "s3cr3t",
            "lang": "pt_br",
            "q": "rio de janeiro",
            "units": "metric",
        },
        "url": "https://api.openweathermap.org/data/2.5/weather",
    }
    assert response == {
        "base": "stations",
        "clouds": 75,
        "cod": 200,
        "country": "BR",
        "deg": 250,
        "description": "nublado",
        "dt": 1664325856,
        "emoji": "🌥",
        "humidity": 82,
        "id": 3451190,
        "lat": -22.9028,
        "lon": -43.2075,
        "main": "Clouds",
        "name": "Rio de Janeiro",
        "pressure": 1015,
        "speed": 3.6,
        "sunrise": 1664267844,
        "sunset": 1664311813,
        "temp": 23.2,
        "temp_feels_like": 23.72,
        "temp_max": 24,
        "temp_min": 21.12,
        "timezone": -10800,
        "type": 1,
        "visibility": 10000,
    }


async def test_weather_with_invalid_icon(mock_response):
    return_value = mock_response(
        data={
            "name": "Rio de Janeiro",
            "weather": [{"icon": "invalid"}],
        }
    )

    with patch("aiohttp.ClientSession.request", return_value=return_value) as mock_response:
        response = await Weather(key="s3cr3t").prediction(location="rio de janeiro")

    assert mock_response.call_count == 1
    assert mock_response.call_args[0] == ("get",)
    assert mock_response.call_args[1] == {
        "params": {
            "appid": "s3cr3t",
            "lang": "pt_br",
            "q": "rio de janeiro",
            "units": "metric",
        },
        "url": "https://api.openweathermap.org/data/2.5/weather",
    }
    assert response == {
        "emoji": "🌤",
        "name": "Rio de Janeiro",
    }
