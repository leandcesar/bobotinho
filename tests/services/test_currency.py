# -*- coding: utf-8 -*-
from unittest.mock import patch

import pytest
from bobotinho.services.currency import Currency


async def test_currency(mock_response):
    return_value = mock_response(data={"rate": 5.1234})

    with patch("aiohttp.ClientSession.request", return_value=return_value) as mock_response:
        response = await Currency(key="s3cr3t").rate(base="brl", quote="usd")

    assert mock_response.call_count == 1
    assert mock_response.call_args[0] == ("get",)
    assert mock_response.call_args[1] == {"headers": {"x-coinapi-key": "s3cr3t"}, "url": "https://rest.coinapi.io/v1/exchangerate/BRL/USD"}
    assert response == 5.1234


async def test_currency_invalid():
    with pytest.raises(ValueError):
        response = await Currency(key="s3cr3t").rate(base="invalid", quote="usd")
    with pytest.raises(ValueError):
        response = await Currency(key="s3cr3t").rate(base="123", quote="usd")
    with pytest.raises(ValueError):
        response = await Currency(key="s3cr3t").rate(base="brl", quote="invalid")
    with pytest.raises(ValueError):
        response = await Currency(key="s3cr3t").rate(base="brl", quote="123")
