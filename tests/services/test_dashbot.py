# -*- coding: utf-8 -*-
from unittest.mock import patch

import pytest
from bobotinho.services.dashbot import Dashbot


async def test_dashbot_received(mock_response):
    return_value = mock_response(status=200)

    with patch("aiohttp.ClientSession.request", return_value=return_value) as mock_response:
        response = await Dashbot(key="s3cr3t").received(id=1, name="name", channel="channel", content="content")

    assert mock_response.call_count == 1
    assert mock_response.call_args[0] == ("post",)
    assert mock_response.call_args[1] == {
        "json": {
            "intent": {
                "confidence": None,
                "name": None,
            },
            "platformJson": {},
            "platformUserJson": {
                "firstName": "name",
                "gender": None,
                "locale": "channel",
                "plataform": None,
                "timezone": "-3",
            },
            "text": "content",
            "userId": 1,
        },
        "params": {
            "apiKey": "s3cr3t",
            "platform": "universal",
            "type": "incoming",
            "v": "11.1.0-rest",
        },
        "url": "https://tracker.dashbot.io/track",
    }
    assert response is True


async def test_dashbot_sent(mock_response):
    return_value = mock_response(status=200)

    with patch("aiohttp.ClientSession.request", return_value=return_value) as mock_response:
        response = await Dashbot(key="s3cr3t").sent(id=1, name="name", channel="channel", content="content")

    assert mock_response.call_count == 1
    assert mock_response.call_args[0] == ("post",)
    assert mock_response.call_args[1] == {
        "json": {
            "intent": {
                "confidence": None,
                "name": None,
            },
            "platformJson": {},
            "platformUserJson": {
                "firstName": "name",
                "gender": None,
                "locale": "channel",
                "plataform": None,
                "timezone": "-3",
            },
            "text": "content",
            "userId": 1,
        },
        "params": {
            "apiKey": "s3cr3t",
            "platform": "universal",
            "type": "outgoing",
            "v": "11.1.0-rest",
        },
        "url": "https://tracker.dashbot.io/track",
    }
    assert response is True
