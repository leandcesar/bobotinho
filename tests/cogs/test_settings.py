# -*- coding: utf-8 -*-
from unittest.mock import AsyncMock, patch

import pytest
from bobotinho.cogs.settings import Settings


@pytest.fixture
def settings(mock_bot):
    return Settings(bot=mock_bot())


@pytest.mark.skip("Not implemented")
async def test_enable(settings):
    # TODO
    ...


@pytest.mark.skip("Not implemented")
async def test_disable(settings):
    # TODO
    ...


@pytest.mark.skip("Not implemented")
async def test_start(settings):
    # TODO
    ...


@pytest.mark.skip("Not implemented")
async def test_stop(settings):
    # TODO
    ...
