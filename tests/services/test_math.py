# -*- coding: utf-8 -*-
from unittest.mock import patch

import pytest
from bobotinho.services.math import Math


async def test_math(mock_response):
    return_value = mock_response(data={"result": 4})

    with patch("aiohttp.ClientSession.request", return_value=return_value) as mock_response:
        response = await Math().evaluate(expression="2 + 2", precision=1)

    assert mock_response.call_count == 1
    assert mock_response.call_args[0] == ("post",)
    assert mock_response.call_args[1] == {'json': {'expr': '2 + 2', 'precision': 1}, 'url': 'https://api.mathjs.org/v4'}
    assert response == 4
