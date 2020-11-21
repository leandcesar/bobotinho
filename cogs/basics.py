# -*- coding: utf-8 -*-

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
        usage="https://bobotinho.herokuapp.com/help",
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

    @command(aliases=["pong"], description="verifique se o bot está online", cooldown=30)
    async def ping(self, ctx):
        if ctx.command.invoked_by == "pong":
            ctx.response = f"@{ctx.author.name}, ping 🏓"
        else:
            ctx.response = f"@{ctx.author.name}, pong 🏓"

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
