# -*- coding: utf-8 -*-
import asyncio
from datetime import datetime, timezone

import pytest
from tortoise.contrib.test import finalizer, initializer
from twitchio import Channel, Context, Message, User

from bobotinho import bot_config
from bobotinho.bot import Bobotinho

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
    initializer(["bobotinho.database.models"], db_url=bot_config.database_url, loop=event_loop)
    request.addfinalizer(finalizer)


def create_bot(params: dict = None) -> Bobotinho:
    if not params:
        params = dict(config=bot_config)
    bot = Bobotinho(**params)
    return bot


def create_twitch_channel(params: dict = None) -> Channel:
    if not params:
        params = dict(name=TEST_CHANNEL_NAME)
    twitch_channel = Channel(ws=None, http=None, **params)
    return twitch_channel


def create_twitch_user(params: dict = None) -> User:
    if not params:
        channel = create_twitch_channel()
        params = dict(
            author=TEST_USER_NAME,
            channel=channel,
            tags={
                "user-id": TEST_USER_ID,
                "color": "#000000",
            },
        )
    twitch_user = User(ws=None, **params)
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
        message = create_message()
        params = dict(
            message=message,
            user=message.author,
            channel=message.channel,
            prefix=TEST_PREFIX,
        )
    ctx = Context(**params)
    ctx.response = None
    return ctx


@pytest.fixture(autouse=True)
def ctx() -> Context:
    ctx = create_ctx()
    return ctx
