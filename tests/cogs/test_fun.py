# -*- coding: utf-8 -*-
from unittest.mock import AsyncMock, patch

import pytest
from bobotinho.cogs.interact import Interact


@pytest.fixture
def interact(mock_bot):
    return Interact(bot=mock_bot())


async def test_hug(interact):
    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        await interact.hug._callback(interact, mock_context, name="bot_name")
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("🤗",)

    mock_context.reset_mock()

    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        mock_context.author.name = "author_name"
        await interact.hug._callback(interact, mock_context, name="author_name")
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("você tentou se abraçar...",)

    mock_context.reset_mock()

    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        await interact.hug._callback(interact, mock_context, name="user_name")
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("você abraçou @user_name 🤗",)


async def test_kiss(interact):
    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        await interact.kiss._callback(interact, mock_context, name="bot_name")
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("😳",)

    mock_context.reset_mock()

    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        mock_context.author.name = "author_name"
        await interact.kiss._callback(interact, mock_context, name="author_name")
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("você tentou se beijar...",)

    mock_context.reset_mock()

    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        await interact.kiss._callback(interact, mock_context, name="user_name")
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("você deu um beijinho em @user_name 😚",)


async def test_pat(interact):
    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        await interact.pat._callback(interact, mock_context, name="bot_name")
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("😊",)

    mock_context.reset_mock()

    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        mock_context.author.name = "author_name"
        await interact.pat._callback(interact, mock_context, name="author_name")
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("você tentou fazer cafuné em si mesmo...",)

    mock_context.reset_mock()

    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        await interact.pat._callback(interact, mock_context, name="user_name")
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("você fez cafuné em @user_name 😊",)


async def test_slap(interact):
    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        await interact.slap._callback(interact, mock_context, name="bot_name")
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("vai bater na mãe 😠",)

    mock_context.reset_mock()

    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        mock_context.author.name = "author_name"
        await interact.slap._callback(interact, mock_context, name="author_name")
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("você se deu um tapa... 😕",)

    mock_context.reset_mock()

    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        await interact.slap._callback(interact, mock_context, name="user_name")
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("você deu um tapa em @user_name 👋",)


async def test_tuck(interact):
    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        await interact.tuck._callback(interact, mock_context, name="bot_name")
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("eu não posso dormir agora...",)

    mock_context.reset_mock()

    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        mock_context.author.name = "author_name"
        await interact.tuck._callback(interact, mock_context, name="author_name")
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("você foi para a cama",)

    mock_context.reset_mock()

    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        await interact.tuck._callback(interact, mock_context, name="user_name")
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("você colocou @user_name na cama 🙂👉🛏",)
