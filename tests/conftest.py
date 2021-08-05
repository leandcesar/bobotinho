# -*- coding: utf-8 -*-
import asyncio
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from tortoise.contrib.test import finalizer, initializer

from twitchio.ext.commands import Context
from twitchio.channel import Channel
from twitchio.message import Message
from twitchio.chatter import Chatter

from bobotinho import config
from bobotinho.bots.twitch import Bot
from bobotinho.cache import TTLOrderedDict

TEST_NOT_NAME = "bobotinho"
TEST_CHANNEL_ID = 1
TEST_CHANNEL_NAME = "channel"
TEST_CHANNEL_COLOR = "#000000"
TEST_USER_ID = 2
TEST_USER_NAME = "user"
TEST_USER_COLOR = "#FFFFFF"
TEST_PREFIX = "%"


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request, event_loop):
    initializer(["bobotinho.database.models"], db_url=config.database_url, loop=event_loop)
    request.addfinalizer(finalizer)


@pytest.fixture(scope="session", autouse=True)
def analytics():
    with patch("bobotinho.apis.analytics.Analytics") as mock:
        mock = AsyncMock()
        yield mock


def create_bot(params: dict = None) -> Bot:
    if not params:
        params = dict(config=config)
    bot = Bot(**params)
    return bot


def create_mocked_bot(params: dict = None) -> Mock:
    if not params:
        params = dict(nick=TEST_NOT_NAME, prefix=TEST_PREFIX, cache=TTLOrderedDict())
    mocked_bot = Mock()
    for name, value in params.items():
        setattr(mocked_bot, name, value)
    return mocked_bot


def create_mocked_user(params: dict = None) -> Mock:
    if not params:
        params = dict(id=TEST_USER_ID, name=TEST_USER_NAME, sponsor=False, mention=True)
    mocked_user = Mock()
    for name, value in params.items():
        setattr(mocked_user, name, value)
    return mocked_user


def create_twitch_channel(params: dict = None) -> Channel:
    if not params:
        params = dict(name=TEST_CHANNEL_NAME)
    twitch_channel = Channel(websocket=MagicMock(), **params)
    return twitch_channel


def create_twitch_user(params: dict = None) -> Chatter:
    if not params:
        params = dict(
            tags={
                "user-id": TEST_USER_ID,
                "display-name": TEST_USER_NAME,
                "color": "#000000",
                "subscriber": False,
                "mod": False,
            },
        )
    twitch_user = Chatter(websocket=MagicMock(), **params)
    return twitch_user


def create_message(params: dict = None) -> Message:
    if not params:
        user = create_twitch_user()
        params = dict(
            author=user,
            channel=user.channel,
            content="test message content",
            tags={"tmi-sent-ts": datetime.timestamp(datetime.utcnow().replace(tzinfo=timezone.utc)) * 1000},
        )
    message = Message(**params)
    return message


def create_ctx(params: dict = None) -> Context:
    if not params:
        bot = create_mocked_bot()
        message = create_message()
        params = dict(
            bot=bot,
            message=message,
            user=message.author,
            channel=message.channel,
            prefix=TEST_PREFIX,
        )
    ctx = Context(**params)
    ctx.response = None
    ctx.user = create_mocked_user()
    return ctx


@pytest.fixture(autouse=True)
def ctx() -> Context:
    ctx = create_ctx()
    return ctx
