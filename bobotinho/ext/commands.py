# -*- coding: utf-8 -*-
from typing import Any, Callable, Coroutine

from twitchio.channel import Channel
from twitchio.ext.commands import Context as TwitchioContext
from twitchio.ext.commands import Bot, Cog, Command, cooldown, command
from twitchio.ext.routines import routine
from twitchio.message import Message
from twitchio.user import User


class Context(TwitchioContext):
    user: Any = None

    def __iter__(self):
        yield "author", self.author.name if self.author and self.author.name else None
        yield "channel", self.channel.name if self.channel and self.channel.name else None
        yield "message", self.message.content if self.message and self.message.content else None
        yield "command", self.command.name if self.command and self.command.name else None


def check(func: Callable[[Context], bool]) -> Callable[[Command], Command]:

    def decorator(command: Command) -> Command:
        if type(command) != Command:
            raise TypeError(f"Expected 'twitchio.ext.commands.Command', not '{type(command)}'")
        command._checks.append(func)
        return command

    return decorator


def usage(usage: str) -> Callable[[Command], Command]:

    def decorator(command: Command) -> Command:
        if type(command) != Command:
            raise TypeError(f"Expected 'twitchio.ext.commands.Command', not '{type(command)}'")
        command.usage = usage
        return command

    return decorator


def helper(description: str) -> Callable[[Command], Command]:

    def decorator(command: Command) -> Command:
        if type(command) != Command:
            raise TypeError(f"Expected 'twitchio.ext.commands.Command', not '{type(command)}'")
        command.description = description
        return command

    return decorator
