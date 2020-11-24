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

import config 
import re


def is_admin(ctx):
    return is_owner(ctx) or is_mod(ctx)


def is_allowed(ctx):
    return is_owner(ctx) or is_sub(ctx) or is_vip(ctx) or is_mod(ctx)


def is_owner(ctx):
    return ctx.author.id == config.Vars.owner_id


def is_mod(ctx):
    return ctx.author.is_mod or ctx.author.name == ctx.channel.name


def is_vip(ctx):
    return ctx.author.badges.get("vip", False)


def is_sub(ctx):
    return ctx.author.is_subscriber


def is_link(message: str):
    return re.search(r"([.0-9a-zA-Z-]*\.[a-z]{2,3}(?:\/\S*))", message)
