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

from twitchio.dataclasses import Context

with open("data//banned.txt", "r", encoding="utf-8") as file:
    banned = [int(x) for x in file.read().split()] # lista de IDs banidos


def is_owner(ctx: Context) -> bool:
    """Verifica se o usuário é o dono do bot."""
    return ctx.author.id == config.Vars.owner_id


def is_mod(ctx: Context) -> bool:
    """Verifica se o usuário é um moderador."""
    return ctx.author.is_mod or ctx.author.name == ctx.channel.name


def is_vip(ctx: Context) -> bool:
    """Verifica se o usuário é um VIP."""
    return ctx.author.badges.get("vip", False)


def is_sub(ctx: Context) -> bool:
    """Verifica se o usuário é um inscrito."""
    return ctx.author.is_subscriber


def is_admin(ctx: Context) -> bool:
    """Verifica se o usuário é o dono do bot ou um moderador."""
    return is_mod(ctx) or is_owner(ctx)


def is_allowed(ctx: Context) -> bool:
    """Verifica se o usuário tem algum cargo."""
    return is_sub(ctx) or is_vip(ctx) or is_mod(ctx) or is_owner(ctx)


def is_link(message: str) -> bool:
    """Verifica se existe um link na mensagem."""
    return re.search(r"([0-9a-zA-Z]*\.[a-zA-Z]{2,3})", message) != None
