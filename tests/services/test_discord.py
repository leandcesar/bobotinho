# -*- coding: utf-8 -*-
from unittest.mock import patch

import pytest
from bobotinho.services.discord import Discord


async def test_discord_webhook(mock_response):
    return_value = mock_response(status=200)

    with patch("aiohttp.ClientSession.request", return_value=return_value) as mock_response:
        response = await Discord(url="url").webhook(name="name", content="content", avatar="avatar")

    assert mock_response.call_count == 1
    assert mock_response.call_args[0] == ("post",)
    assert mock_response.call_args[1] == {
        "json": {
            "avatar_url": "avatar",
            "content": "content",
            "username": "name",
        },
        "url": "url",
    }
    assert response is True
