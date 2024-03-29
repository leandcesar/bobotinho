# -*- coding: utf-8 -*-
from unittest.mock import AsyncMock, patch

import pytest
from bobotinho.cogs.rand import Rand


@pytest.fixture
def rand(mock_bot):
    return Rand(bot=mock_bot())


async def test_joke(rand):
    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        await rand.joke._callback(rand, mock_context)
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("Sabe porque o rapaz jogou o computador no mar? Pra ele navegar na internet 4Head",)


async def test_sadcat(rand):
    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        await rand.randomsadcat._callback(rand, mock_context)
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("https://i.imgur.com/tcA50wO.jpg 😿",)
