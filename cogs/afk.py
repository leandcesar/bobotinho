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
import re

from ext.command import command
from twitchio.ext import commands
from utils import convert, checks

quotes = dict(
    # alias = (default_message, %afk, %isafk, returned, %rafk)
    afk=("🏃⌨", "ficou afk", "está afk", "voltou", "continuou afk"),
    art=("🎨", "foi desenhar", "está desenhando", "desenhou", "continuou desenhando"),
    brb=("🏃⌨", "volta logo", "volta logo", "voltou", "volta logo"),
    code=("💻", "foi programar", "está programando", "programou", "volta logo"),
    food=("🍽", "foi comer", "está comendo", "comeu", "continuou comendo"),
    game=("🎮", "foi jogar", "está jogando", "parou de jogar", "voltou a jogar"),
    gn=("😪💤", "foi dormir", "está dormindo", "acordou", "continuou dormindo"),
    work=("💼", "foi trabalhar", "está trabalhando", "trabalhou", "continuou trabalhando"),
    shower=("☺🚿", "foi pro banho", "está no banho", "tomou banho", "continuou seu banho"),
    study=("📚", "foi estudar", "está estudando", "estudou", "continuou estudando"),
)


def aliases():
    return list(quotes.keys())[1:]


def raliases():
    return ["r" + alias for alias in list(quotes.keys())[1:]]


def default_message(alias):
    return quotes[alias.replace("\r", "")][0]


def quote_afk(alias):
    return quotes[alias.replace("\r", "")][1]


def quote_isafk(alias):
    return quotes[alias.replace("\r", "")][2]


def quote_returned(alias):
    return quotes[alias.replace("\r", "")][3]


def quote_rafk(alias):
    return quotes[alias.replace("\r", "")][4]


class Afk(commands.AutoCog):
    def __init__(self, bot):
        self.bot = bot

    def _prepare(self, bot):
        pass

    @command(
        aliases=aliases(),
        description="informe que você está se ausentando do chat",
        cooldown=15,
    )
    async def afk(self, ctx, *, message: str = None):
        if not message:
            message = default_message(ctx.command.invoked_by)
        if len(message) > 300:
            ctx.response = f"@{ctx.author.name}, essa mensagem é muito comprida"
        elif not checks.is_allowed(ctx) and checks.is_link(message):
            ctx.response = f"@{ctx.author.name}, apenas inscritos, vips e moderadores podem enviar links"
        else:
            await self.bot.db.update(
                "users",
                values={"afk": ctx.command.invoked_by},
                where={"id": ctx.author.id},
            )
            ctx.response = (
                f"@{ctx.author.name} {quote_afk(ctx.command.invoked_by)}: {message}"
            )

    @command(
        description="verifique se alguém está afk",
        usage="digite o comando e o nome do usuário para saber se ele está afk",
    )
    async def isafk(self, ctx, user: str):
        user = convert.user(user)
        if user == self.bot.nick:
            ctx.response = f"@{ctx.author.name}, eu sempre estou aqui... observando"
        elif user == ctx.author.name:
            ctx.response = f"@{ctx.author.name}, você não está afk... obviamente"
        else:
            row = await self.bot.db.select("users", where={"name": user})
            if not row:
                ctx.response = (
                    f"@{ctx.author.name}, @{user} ainda não foi registrado "
                    f"(o usuário precisa ter usado algum comando)"
                )
            elif not row["afk"]:
                ctx.response = f"@{ctx.author.name}, @{user} não está afk"
            else:
                timesince = convert.timesince(row["timestamp"], ctx.message.timestamp)
                message = row["message"].replace(f'{ctx.prefix}{row["afk"]}', "", 1)
                if not message:
                    message = default_message(row["afk"])
                ctx.response = f'@{ctx.author.name}, @{user} {quote_isafk(row["afk"])}: {message} ({timesince})'

    @command(
        aliases=["ls"],
        description="saiba a última vez que alguém foi visto",
        cooldown=10,
        usage="digite o comando e o nome de alguém para saber quando foi visto pela última vez",
    )
    async def lastseen(self, ctx, user: str):
        ctx.response = (
            f"@{ctx.author.name}, comando temporariamente desativado"
        )
        return
        user = convert.user(user)
        if user == self.bot.nick:
            ctx.response = (
                f"@{ctx.author.name}, estou em todos os lugares, a todo momento..."
            )
        elif user == ctx.author.name:
            ctx.response = f"@{ctx.author.name}, você foi visto pela última vez aqui: {ctx.content} ({convert.timesince(ctx)})"
        else:
            row = await self.bot.db.select(
                "users", what=["channel", "message", "timestamp"], where={"name": user}
            )
            if not row:
                ctx.response = (
                    f"@{ctx.author.name}, @{user} ainda não foi registrado "
                    "(o usuário precisa ter usado algum comando)"
                )
            else:
                timesince = convert.timesince(row["timestamp"], ctx.message.timestamp)
                if not row["message"] and not row["channel"]:
                    ctx.response = f"@{ctx.author.name}, @{user} foi visto pela última vez há {timesince}"
                elif not row["channel"]:
                    ctx.response = f'@{ctx.author.name}, @{user} foi visto pela última vez: {row["message"]} ({timesince})'
                elif not row["message"]:
                    ctx.response = f'@{ctx.author.name}, @{user} foi visto em @{row["channel"]} pela última vez ({timesince})'
                else:
                    ctx.response = f'@{ctx.author.name}, @{user} foi visto  em @{row["channel"]} pela última vez: {row["message"]} ({timesince})'

    @command(
        aliases=raliases(),
        description="retome seu status de ausência do chat",
        cooldown=15,
        usage="digite o comando em até 3 minutos após ter retornado do seu afk para retomá-lo",
    )
    async def rafk(self, ctx):
        global returned_afk
        returned = returned_afk.pop(ctx.author.id, None)
        if not returned:
            return
        await self.bot.db.update(
            "users",
            values={
                "afk": ctx.command.invoked_by[1:], 
                "timestamp": returned["timestamp"],
                "message": ctx.command.invoked_by + " " + returned["message"], 
                },
            where={"id": ctx.author.id},
        )
        ctx.response = (
            f'@{ctx.author.name} {quote_rafk(ctx.command.invoked_by[1:])}: {returned["message"]}'
        )


returned_afk = dict()


async def returned(bot, message, send: bool = True):
    if bot.channels.is_disabled(message.channel.name, "afk"):
        return

    row = await bot.db.select("users", where={"id": message.author.id})
    if not row or not row["afk"]:
        return

    timesince = convert.timesince(row["timestamp"])
    if not checks.is_allowed(message) and checks.is_link(row["message"]):
        _message = "(a mensagem continha um link e o usuário não é inscrito, vip ou moderador)"
    elif " " in row["message"]:
        _message = row["message"].partition(" ")[2]
    else:
        _message = default_message(row["afk"])
    response = f'@{message.author.name} {quote_returned(row["afk"])}: {_message} ({timesince})'
    
    await bot.db.update("users", values={"afk": None}, where={"id": message.author.id})

    global returned_afk
    returned_afk = {
        k: v 
        for k, v in returned_afk.items() 
        if v["timestamp"] + datetime.timedelta(seconds=180) > message.timestamp
    }
    returned_afk[message.author.id] = {"message": _message, "timestamp": row["timestamp"]}
    
    if send and not bot.channels.is_banword(message.channel.name, response):
        await message.channel.send(response)
        bot.log.info(
            f"#{message.channel.name} {message.author.name}: {message.content} > {response}"
        )
        return True


def prepare(bot):
    bot.add_cog(Afk(bot))


def breakdown(bot):
    pass
