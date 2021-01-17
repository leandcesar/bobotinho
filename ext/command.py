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

import time
from twitchio.ext import commands

DEFAULT_COOLDOWN = 5  # in seconds


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


holder = {}
max_lenght = 512

def cooldown(ctx):
    global holder
    now = time.monotonic()
    holder = {k: v for k, v in holder.items() if v > now}
    if len(holder) >= max_lenght:
        del holder[list(holder.keys())[0]]
    key = f"{ctx.author.id}-{ctx.command.name}"
    if key in holder:
        return False
    else:
        holder[key] = time.monotonic() + ctx.command.cooldown
        return True
