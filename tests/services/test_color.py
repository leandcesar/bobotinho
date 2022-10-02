# -*- coding: utf-8 -*-
from unittest.mock import patch

import pytest
from bobotinho.services.color import Color


async def test_color(mock_response):
    return_value = mock_response(data={"name": {"value": "white"}})

    with patch("aiohttp.ClientSession.request", return_value=return_value) as mock_response:
        response = await Color().hex_to_name(code="#ffffff")

    assert mock_response.call_count == 1
    assert mock_response.call_args[0] == ("get",)
    assert mock_response.call_args[1] == {"params": {"hex": "FFFFFF"}, "url": "https://www.thecolorapi.com/id"}
    assert response == "white"


async def test_color_invalid():
    with pytest.raises(ValueError):
        response = await Color().hex_to_name(code="invalid")
    with pytest.raises(ValueError):
        response = await Color().hex_to_name(code="#fffffz")
    with pytest.raises(ValueError):
        response = await Color().hex_to_name(code="#11111")
