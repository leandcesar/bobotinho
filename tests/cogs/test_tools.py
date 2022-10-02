# -*- coding: utf-8 -*-
from unittest.mock import AsyncMock, patch

import pytest
from bobotinho.cogs.tools import Tools


@pytest.fixture
def tools(mock_bot):
    return Tools(bot=mock_bot())


@pytest.mark.skip("Not implemented")
async def test_currency(tools):
    # TODO
    ...


@pytest.mark.skip("Not implemented")
async def test_dolar(tools):
    # TODO
    ...


@pytest.mark.skip("Not implemented")
async def test_math(tools):
    # TODO
    ...


@pytest.mark.skip("Not implemented")
async def test_translate(tools):
    # TODO
    ...


@pytest.mark.skip("Not implemented")
async def test_weather(tools):
    # TODO
    ...
