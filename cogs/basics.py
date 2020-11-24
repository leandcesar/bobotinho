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
import datetime
import os
import psutil

from ext.command import command
from twitchio.ext import commands
from utils import convert


class Basics(commands.AutoCog):
    def __init__(self, bot):
        self.bot = bot
        self.boot = datetime.datetime.utcnow()

    def _prepare(self, bot):
        pass

    @command(aliases=["bot"], description="veja as principais informações sobre o bot", cooldown=30)
    async def botinfo(self, ctx):
        channels = len(self.bot.channels)
        commands = len(self.bot.commands)
        owner = config.Vars.owner_nick
        language = "Python"
        library = "TwitchIO"
        database = "PostgreSQL"
        host = "Heroku"
        process = psutil.Process()
        ram = process.memory_full_info().rss / 1024.0 ** 2

        ctx.response = (
            f"@{ctx.author.name}, conectado à {channels} canais, {commands} comandos, "
            f"feito por @{owner} em {language} com {library} e {database}, "
            f"hospedado em {host} e usando {ram:.1f}MB de RAM"
        )
    @command(
        aliases=["commands"],
        description="veja a lista de comandos ou como utilizar um comando específico",
        cooldown=2,
        usage="veja a lista de comandos aqui: https://bobotinho.herokuapp.com/help",
    )
    async def help(self, ctx, command: str):
        def get_command(command: str):
            command = convert.command(command)
            for c in self.bot.commands.values():
                if command == c.name or (c.aliases and command in c.aliases):
                    return c
        c = get_command(command)
        if not c:
            return
        elif self.bot.channels.is_disabled(ctx.channel.name, c.name):
            ctx.response = f"@{ctx.author.name}, esse comando está desativado"
        elif c.aliases:
            ctx.response = (
                f"@{ctx.author.name}, {ctx.prefix}{c.name} "
                f'({ctx.prefix}{f", {ctx.prefix}".join(c.aliases)}): '
                f"{c.description} - {c.cooldown}s cooldown"
            )
        else:
            ctx.response = (
                f"@{ctx.author.name}, {ctx.prefix}{c.name}: "
                f"{c.description} - {c.cooldown}s cooldown"
            )

    @command(description="receba o link para adicionar o bot no seu chat", cooldown=30)
    async def invite(self, ctx):
        ctx.response = f"@{ctx.author.name}, me adicione no seu chat: https://bobotinho.herokuapp.com/invite"

    @command(aliases=["pong"], description="verifique se o bot está online", cooldown=30)
    async def ping(self, ctx):
        if ctx.command.invoked_by == "pong":
            ctx.response = f"@{ctx.author.name}, ping 🏓"
        else:
            ctx.response = f"@{ctx.author.name}, pong 🏓"

    @command(
        aliases=["discord", "github", "twitter"],
        description="receba o link do site do bot para mais informações", 
        cooldown=30
    )
    async def site(self, ctx):
        ctx.response = f"@{ctx.author.name}, mais informações no meu site: https://bobotinho.herokuapp.com/"

    @command(
        description="faça uma sugestão de recurso para o bot",
        cooldown=15,
        usage="digite o comando e uma sugestão de recurso ou modificação para o bot",
    )
    async def suggest(self, ctx, *, suggestion: str):
        await self.bot.db.insert(
            "suggests",
            values={
                "name": ctx.author.name,
                "channel": ctx.channel.name,
                "message": suggestion,
                "timestamp": ctx.message.timestamp,
            },
        )
        ctx.response = f"@{ctx.author.name}, sua sugestão foi anotada"

    @command(description="verifique há quanto tempo o bot está online", cooldown=30)
    async def uptime(self, ctx):
        uptime = convert.timesince(self.boot)
        ctx.response = f"@{ctx.author.name}, {uptime} desde a última inicialização"


def prepare(bot):
    bot.add_cog(Basics(bot))


def breakdown(bot):
    pass
