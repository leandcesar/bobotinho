# -*- coding: utf-8 -*-

"""
bobotinho - Twitch bot for Brazilian offstream chat entertainment
Copyright (C) 2020  Leandro César

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import datetime
from twitchio.ext import commands

DEFAULT_COOLDOWN = 5  # in seconds
MAX_CACHE = 256


class Command(commands.Command):
    def __init__(self, name: str, func, **attrs):
        self.description = attrs.pop("description")
        self.cooldown = attrs.pop("cooldown", DEFAULT_COOLDOWN)
        self.level = attrs.pop("level", "viewer")
        self.usage = attrs.pop("usage", None)
        super().__init__(name, func, **attrs)


def command(name: str = None, aliases: list = None, no_global_checks: bool = False, **attrs):
    def decorator(func):
        fname = name or func.__name__
        command = Command(
            fname, func, aliases=aliases, no_global_checks=no_global_checks, **attrs
        )

        return command

    return decorator


on_hold = dict()


def cooldown(ctx):
    global on_hold
    on_hold = {
        k: v for k, v in on_hold.items() if v > ctx.message.timestamp
    }
    key = f"{ctx.author.name}-{ctx.channel.name}-{ctx.command.name}"
    if key in on_hold:
        return False
    if len(on_hold) >= MAX_CACHE:
        del on_hold[list(on_hold.keys())[0]]
    on_hold[key] = ctx.message.timestamp + datetime.timedelta(seconds=ctx.command.cooldown)
    return True
