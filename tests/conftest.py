# -*- coding: utf-8 -*-
import random
from typing import Optional

import pytest

random.seed(0)


class MockResponse:
    def __init__(self, *, data: dict, status: int):
        self._data = data
        self.status = status

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        pass

    async def json(self) -> dict:
        if not self.ok:
            raise Exception
        return self._data

    @property
    def ok(self) -> bool:
        return 200 <= self.status < 300


class MockClientSession:
    def __init__(self, *, response: MockResponse):
        self._response = response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        pass

    def request(self, *args, **kwargs) -> MockResponse:
        return self._response


class MockCommand:
    def __init__(self, *, name: str, aliases: list[str], description: str):
        self.name = name
        self.aliases = aliases
        self.description = description


class MockBot:
    def __init__(self, *, nick: str, prefix: str, connected_channels: list[str], commands: list[MockCommand]):
        self.nick = nick
        self.connected_channels = connected_channels
        self.commands = commands
        self._prefix = prefix

    def get_command(self, name: str) -> Optional[MockCommand]:
        for command in self.commands:
            if name == command.name:
                return command
        return None


@pytest.fixture
def mock_session():

    def _mock_session(response: MockResponse = MockResponse(data={}, status=200)):
        return MockClientSession(response=response)

    return _mock_session


@pytest.fixture
def mock_response():

    def _mock_response(data: dict = {}, status: int = 200):
        return MockResponse(data=data, status=status)

    return _mock_response


@pytest.fixture
def mock_command():

    def _mock_command(
        name: str = "command_name",
        aliases: list[str] = ["cmd_alias"],
        description: str = "description",
    ):
        return MockCommand(name=name, aliases=aliases, description=description)

    return _mock_command


@pytest.fixture
def mock_bot():

    def _mock_bot(
        nick: str = "bot_name",
        prefix: str = "%",
        connected_channels: list[str] = [],
        commands: list[MockCommand] = [MockCommand(name="command_name", aliases=["cmd_alias"], description="description")],
    ):
        return MockBot(nick=nick, prefix=prefix, connected_channels=connected_channels, commands=commands)

    return _mock_bot
