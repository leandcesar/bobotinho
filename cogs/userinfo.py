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

import random
import re

from ext.command import command
from twitchio.ext import commands
from utils import asyncrq, convert


async def _get_response(route: str):
    try:
        response = await asyncrq.get("https://decapi.me/twitch" + route, res_method="text")
    except:
        return None
    else:
        if response == "404 Page Not Found":
            return None
        return response


async def get_accountage(channel: str):
    route = f"/accountage/{channel}?lang=pt&precision=4"
    response = await _get_response(route)
    if not response:
        return None
    elif response == f'No user with the name "{channel}" found.':
        return f"@{channel} não existe"
    else:
        return response.replace(",", "")


async def get_creation(channel: str):
    route = f"/creation/{channel}?format=d/m/Y%20\à\s%20H:i:s&tz=America/Sao_Paulo"
    response = await _get_response(route)
    if not response:
        return None
    elif response == f'No user with the name "{channel}" found.':
        return f"@{channel} não existe"
    else:
        return response


async def get_follow(channel: str, user: str):
    route = f"/followed/{channel}/{user}?format=d/m/Y%20\à\s%20H:i:s&tz=America/Sao_Paulo"
    response = await _get_response(route)
    if not response:
        return None
    dont_follow = ("cannot follow", "does not", "not found", "Not Found", "No user")
    return not any(x in response for x in dont_follow)


async def get_followage(channel: str, user: str):
    route = f"/followage/{channel}/{user}?lang=pt&precision=4"
    response = await _get_response(route)
    if not response:
        return None
    elif response == f'No user with the name "{user}" found.':
        return f"@{user} não existe"
    elif response == f'No user with the name "{channel}" found.':
        return f"@{channel} não existe"
    elif response == "Follow not found":
        return False
    elif response == "A user cannot follow themself.":
        return False
    else:
        return response.replace(",", "")


async def get_followcount(channel: str):
    route = f"/followcount/{channel}"
    response = await _get_response(route)
    if not response:
        return None
    elif response == f'No user with the name "{channel}" found.':
        return f"@{channel} não existe"
    else:
        return response


async def get_followed(channel: str, user: str):
    route = f"/followed/{channel}/{user}?format=d/m/Y%20\à\s%20H:i:s&tz=America/Sao_Paulo"
    response = await _get_response(route)
    if not response:
        return None
    elif response == f'No user with the name "{user}" found.':
        return f"@{user} não existe"
    elif response == f'No user with the name "{channel}" found.':
        return f"@{channel} não existe"
    elif response == "Follow not found":
        return False
    elif response == "A user cannot follow themself.":
        return False
    else:
        return response


async def get_followers(channel: str, count: int = 1):
    route = f"/followers/{channel}?direction=asc&count={count}"
    response = await _get_response(route)
    if not response:
        return None
    elif response == f'No user with the name "{channel}" found.':
        return f"@{channel} não existe"
    elif response == "You do not have any followers :(":
        return False
    else:
        return response.lower()


async def get_following(channel: str, limit: int = 1):
    route = f"/following/{channel}?direction=asc&limit={limit}"
    response = await _get_response(route)
    if not response:
        return None
    elif response == f'No user with the name "{channel}" found.':
        return f"@{channel} não existe"
    elif response == "End of following list.":
        if limit == 1:
            return await get_following(channel, limit=2)
        return False
    else:
        return response.lower()


class UserInfo(commands.AutoCog):
    def __init__(self, bot):
        self.bot = bot

    def _prepare(self, bot):
        pass

    @staticmethod
    def _is_birthday(date: str):
        return "ano" in date and not any(
            x in date for x in ("mês", "meses", "semana", "dia")
        )

    @staticmethod
    def _user_format(ctx, name: str):
        return "você" if name == ctx.author.name else f"@{name}"

    @staticmethod
    async def _color_name(color):
        req = await asyncrq.get("https://www.thecolorapi.com/id?hex=" + color[1:])
        return req["name"]["value"]

    @command(
        aliases=["accage", "age"],
        description="saiba há quanto tempo algum usuário criou sua conta",
    )
    async def accountage(self, ctx, user: str = None):
        if not user:
            user = ctx.author.name

        user = convert.user(user)
        accountage = await get_accountage(user)
        user = self._user_format(ctx, user)

        if user == f"@{self.bot.nick}":
            ctx.response = f"@{ctx.author.name}, eu sempre existi..."
        elif accountage is None:
            ctx.response = f"@{ctx.author.name}, não foi possível verificar isso"
        elif "não existe" in accountage:
            ctx.response = f"@{ctx.author.name}, {accountage}"
        elif self._is_birthday(accountage):
            accountage = " ".join(accountage.split()[:2])
            ctx.response = f"@{ctx.author.name}, hoje completa {accountage} que {user} criou a conta 🎂"
        else:
            ctx.response = f"@{ctx.author.name}, {user} criou a conta há {accountage}"

    @command(description="saiba quando algum usuário criou sua conta")
    async def creation(self, ctx, user: str = None):
        if not user:
            user = ctx.author.name

        user = convert.user(user)
        creation = await get_creation(user)
        user = self._user_format(ctx, user)

        if user == f"@{self.bot.nick}":
            ctx.response = f"@{ctx.author.name}, eu sempre existi..."
        elif creation is None:
            ctx.response = f"@{ctx.author.name}, não foi possível verificar isso"
        elif "não existe" in creation:
            ctx.response = f"@{ctx.author.name}, {creation}"
        else:
            ctx.response = f"@{ctx.author.name}, {user} criou a conta em {creation}"

    @command(description="saiba o código hexadecimal da cor de algum usuário")
    async def color(self, ctx, user: str = None):
        if not user:
            user = ctx.author.name

        user = convert.user(user)

        if user == ctx.author.name:
            color = ctx.author.colour
            name = await self._color_name(color)
            ctx.response = f"@{ctx.author.name}, sua cor é {color}, {name}"
            saved_color = await self.bot.db.select1(
                "users", what="saved_color", where={"id": ctx.author.id}
            )
            if saved_color:
                ctx.response += f" (cor salva: {saved_color})"
        elif user == self.bot.nick:
            ctx.response = f"@{ctx.author.name}, minha cor é #FFFFFF, White"
        elif user == "random":
            color = f"#{random.randint(0, 0xFFFFFF):06X}"
            ctx.response = f"@{ctx.author.name}, aqui está uma cor aleatória: {color}"
        elif re.match(r"#(?:[0-9A-Fa-f]{6})$", user):
            color = user
            name = await self._color_name(color)
            ctx.response = f"@{ctx.author.name}, {color.upper()}, {name}"
        else:
            color = await self.bot.db.select1(
                "users", what="color", where={"name": user}
            )
            if not color:
                ctx.response = (
                    f"@{ctx.author.name}, @{user} ainda não foi registrado "
                    f"(o usuário precisa ter usado algum comando)"
                )
            elif color == "#F8A6E9":
                ctx.response = f"@{ctx.author.name}, rosa."
            elif color == "#A6F8AA":
                ctx.response = f"@{ctx.author.name}, verde."
            else:
                name = await self._color_name(color)
                ctx.response = (
                    f"@{ctx.author.name}, a cor de @{user} é {color}, {name}"
                )
    
    @command(
        aliases=["ff"],
        description="saiba o primeiro seguidor e o primeiro canal seguido de algum usuário",
    )
    async def firstfollow(self, ctx, user: str = None):
        if not user:
            user = ctx.author.name

        user = convert.user(user)
        following = await get_following(user)
        follower = await get_followers(user)
        user = self._user_format(ctx, user)

        if following is None:
            ctx.response = f"@{ctx.author.name}, não foi possível verificar isso"
        elif isinstance(following, str) and "não existe" in following:
            ctx.response = f"@{ctx.author.name}, {following}"
        elif following and follower:
            ctx.response = (
                f"@{ctx.author.name}, {user} seguiu primeiro @{following} e "
                f"foi seguido primeiro por @{follower}"
            )
        elif following and not follower:
            ctx.response = (
                f"@{ctx.author.name}, {user} seguiu primeiro @{following} e "
                f"não é seguido por ninguém"
            )
        elif not following and follower:
            ctx.response = (
                f"@{ctx.author.name}, {user} não segue ninguém e "
                f"foi seguido primeiro por @{follower}"
            )
        else:
            ctx.response = (
                f"@{ctx.author.name}, {user} não segue e não é seguido por ninguém"
            )

    @command(
        aliases=["fa"],
        description="saiba há quanto tempo algum usuário segue algum canal",
    )
    async def followage(self, ctx, user: str = None, channel: str = None):
        if not user:
            user = ctx.author.name
        if not channel:
            channel = ctx.channel.name

        user = convert.user(user)
        channel = convert.user(channel)
        followage = await get_followage(channel, user)
        user = self._user_format(ctx, user)
        channel = self._user_format(ctx, channel)

        if user == f"@{self.bot.nick}":
            ctx.response = f"@{ctx.author.name}, eu sempre estive aqui..."
        elif followage is None:
            ctx.response = f"@{ctx.author.name}, não foi possível verificar isso"
        elif not followage:
            ctx.response = f"@{ctx.author.name}, {user} não segue {channel}"
        elif "não existe" in followage:
            ctx.response = f"@{ctx.author.name}, {followage}"
        elif self._is_birthday(followage):
            followage = " ".join(followage.split()[:2])
            ctx.response = f"@{ctx.author.name}, hoje completa {followage} que {user} segue {channel} 🎂"
        else:
            ctx.response = f"@{ctx.author.name}, {user} segue {channel} há {followage}"

    @command(description="saiba quando algum usuário seguiu algum canal")
    async def followed(self, ctx, user: str = None, channel: str = None):
        if not user:
            user = ctx.author.name
        if not channel:
            channel = ctx.channel.name

        user = convert.user(user)
        channel = convert.user(channel)
        followed = await get_followed(channel, user)
        user = self._user_format(ctx, user)
        channel = self._user_format(ctx, channel)

        if user == f"@{self.bot.nick}":
            ctx.response = f"@{ctx.author.name}, eu sempre estive aqui..."
        elif followed is None:
            ctx.response = f"@{ctx.author.name}, não foi possível verificar isso"
        elif not followed:
            ctx.response = f"@{ctx.author.name}, {user} não segue {channel}"
        elif "não existe" in followed:
            ctx.response = f"@{ctx.author.name}, {followed}"
        else:
            ctx.response = f"@{ctx.author.name}, {user} seguiu {channel} em {followed}"

    @command(description="salve a sua cor atual ou algum código hexadecimal")
    async def savecolor(self, ctx, color: str = None):
        if not color:
            color = ctx.author.colour
        if not re.match(r"#(?:[0-9A-Fa-f]{6})$", color):
            ctx.response = (
                f"@{ctx.author.name}, {color} não é um código hexadecimal de cor válido"
            )
        else:
            await self.bot.db.update(
                "users", values={"saved_color": color.upper()}, where={"id": ctx.author.id}
            )
            ctx.response = (
                f"@{ctx.author.name}, você salvou a cor {color.upper()} "
                f"e pode visualizá-la usando {ctx.prefix}color"
            )


def prepare(bot):
    bot.add_cog(UserInfo(bot))


def breakdown(bot):
    pass
