# -*- coding: utf-8 -*-
from unittest.mock import AsyncMock, patch

import pytest
from bobotinho.cogs.misc import Misc


@pytest.fixture
def misc(mock_bot, mock_session):
    return Misc(bot=mock_bot(), session=mock_session())


async def test_botinfo(misc):
    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        await misc.botinfo._callback(misc, mock_context)
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("estou conectado à 0 canais, com 1 comandos, feito por @discretinho com TwitchIO",)


async def test_bug(misc):
    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        await misc.bug._callback(misc, mock_context, content="content")
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("seu bug foi reportado 🐛",)


async def test_help(misc):
    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        await misc.help._callback(misc, mock_context, content="content")
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("veja todos os comandos: https://test.com/docs/help",)

    mock_context.reset_mock()

    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        await misc.help._callback(misc, mock_context)
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("veja todos os comandos: https://test.com/docs/help",)

    mock_context.reset_mock()

    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        await misc.help._callback(misc, mock_context, content="command_name")
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("%command_name (%cmd_alias): description",)


async def test_invite(misc):
    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        await misc.invite._callback(misc, mock_context)
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("me adicione no seu chat: https://test.com/invite",)


async def test_ping(misc):
    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        await misc.ping._callback(misc, mock_context)
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("pong 🏓",)


async def test_site(misc):
    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        await misc.site._callback(misc, mock_context)
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("acesse: https://test.com",)


async def test_suggest(misc):
    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        await misc.suggest._callback(misc, mock_context, content="content")
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("sua sugestão foi anotada 💡",)


async def test_uptime(misc):
    with patch("twitchio.ext.commands.core.Context", new_callable=AsyncMock) as mock_context:
        await misc.uptime._callback(misc, mock_context)
        assert mock_context.reply.await_count == 1
        assert mock_context.reply.await_args[0] == ("eu estou ligado há pouco tempo",)
