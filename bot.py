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
import inspect
import logging
import os

from cogs import afk, remind
from ext import command, channels, postgresql
from twitchio.ext import commands
from utils import checks, convert

logging.basicConfig(
    level=logging.ERROR,
    format='[%(levelname)s] "%(module)s.py", line %(lineno)s, in %(funcName)s: %(message)s',
)


class Bobotinho(commands.Bot):
    def __init__(self):
        self.log = logging.getLogger()
        super().__init__(
            irc_token=config.Vars.tmi_token,
            client_id=config.Vars.client_id,
            client_secret=config.Vars.client_secret,
            prefix=config.Vars.prefix,
            nick=config.Vars.bot_nick,
            initial_channels=[config.Vars.bot_nick],
        )

    async def event_error(self, err, data=None):
        self.log.error(convert.traceback(err))

    async def event_command_error(self, ctx, err):
        if isinstance(err, commands.CheckFailure) and str(err).split()[-1] == "is_enabled":
            response = f"@{ctx.author.name}, {ctx.prefix}{ctx.command.name} está desativado nesse canal"
            await ctx.send(response)
        elif isinstance(err, (commands.CommandNotFound, commands.CheckFailure)):
            pass
        elif isinstance(err, commands.MissingRequiredArgument) and ctx.command.usage:
            ctx.response = f"@{ctx.author.name}, {ctx.command.usage}"
        else:
            self.log.error(convert.traceback(err))

    async def join_all_channels(self):
        all_channels = await self.db.select_all("channels")
        self.channels = channels.Channels(all_channels)
        await self.join_channels(list(self.channels))

    def load_all_modules(self, path: str = "cogs"):
        for module in [filename[:-3] for filename in os.listdir(path) if filename.endswith(".py")]:
            if module == "__init__":
                continue
            try:
                self.load_module(f"{path}.{module}")
            except Exception as err:
                self.log.error(convert.traceback(err))

    async def _handle_checks(self, ctx, no_global_checks=False):
        if no_global_checks:
            checks = ctx.command._checks
        else:
            checks = self._checks + ctx.command._checks
        if not checks:
            return True
        for predicate in checks:
            if inspect.iscoroutinefunction(predicate):
                result = await predicate(ctx)
            else:
                result = predicate(ctx)
            if not result:
                return predicate
        return True

    def add_all_checks(self):
        self.add_check(self.channels.is_enabled)
        self.add_check(self.channels.is_not_banword)
        self.add_check(checks.is_not_banned)
        self.add_check(command.cooldown)

    async def event_ready(self):
        self.db = await postgresql.PostgreSQL.init(config.Vars.database, loop=self.loop)
        await self.join_all_channels()
        self.load_all_modules()
        self.add_all_checks()
        self.log.info(f"{self.nick} | {len(self.channels)} canais | {len(self.commands)} comandos")

    async def global_before_hook(self, ctx):
        await self.db.upsert(
            "users",
            pkey="id",
            values={
                "id": ctx.author.id,
                "name": ctx.author.name,
                "channel": ctx.channel.name,
                "message": ctx.message.content,
                "timestamp": ctx.message.timestamp,
                "color": ctx.author.colour,
            },
        )
        ctx.command.invoked_by = ctx.content.partition(" ")[0][len(ctx.prefix):]

    async def global_after_hook(self, ctx):
        if not hasattr(ctx, "response") and ctx.command.usage:
            ctx.response = f"@{ctx.author.name}, {ctx.command.usage}"
            await ctx.send(ctx.response)
        elif not hasattr(ctx, "response"):
            self.log.error(f'"{ctx.content}" não contém `ctx.response`')
            return
        elif not self.channels.is_not_banword(ctx):
            return
        else:
            await ctx.send(ctx.response)

    async def event_message(self, message):
        if self.channels.is_offline(message):
            await afk.returned(self, message, send=False)
        elif (
            message.author.name == self.nick
            or await afk.returned(self, message)
            or await remind.reminder(self, message)
        ):
            pass
        elif await self.channels[message.channel.name].pyramid.update(message):
            pass
        else:
            await self.handle_commands(convert.case_insensitive(message))


def main():
    bot = Bobotinho()
    bot.run()


if __name__ == "__main__":
    main()
