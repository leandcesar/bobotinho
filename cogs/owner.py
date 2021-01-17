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

import asyncio

from ext.command import command
from ext.channels import Channel
from twitchio.ext import commands
from utils import asyncrq, convert, checks


class Owner(commands.AutoCog):
    def __init__(self, bot):
        self.bot = bot

    def _prepare(self, bot):
        pass

    @command(
        level="owner",
        description="adicione o bot em um canal",
        cooldown=0,
        usage="digite o comando e o nome do canal",
    )
    @commands.check(checks.is_owner)
    async def join(self, ctx, channel: str, id: int):
        channel = convert.user(channel)
        if channel in self.bot.channels:
            ctx.response = f"@{ctx.author.name}, já estou conectado ao canal @{channel}"
        else:
            try:
                await self.bot.join_channels([channel])
                await self.bot.db.insert(
                    "channels",
                    values={
                        "id": int(id),
                        "name": channel,
                        "follows": 0,
                    },
                )
                self.bot.channels[channel] = Channel()
                ctx.response = f"@{ctx.author.name}, me conectei ao canal @{channel}"
            except Exception as err:
                self.bot.log.error(convert.traceback(err))
                ctx.response = f"@{ctx.author.name}, não consegui me conectar ao canal @{channel}"

    @command(
        level="owner",
        description="remova o bot em um canal",
        cooldown=0,
        usage="digite o comando e o nome do canal",
    )
    @commands.check(checks.is_owner)
    async def part(self, ctx, channel: str):
        channel = convert.user(channel)
        if not channel in self.bot.channels:
            ctx.response = f"@{ctx.author.name}, não estou conectado ao canal @{channel}"
        else:
            try:
                await self.bot.part_channels([channel])
                await self.bot.db.delete("channels", where={"name": channel})
                del self.bot.channels[channel]
                ctx.response = f"@{ctx.author.name}, me desconectei do canal @{channel}"
            except Exception as err:
                self.bot.log.error(convert.traceback(err))
                ctx.response = f"@{ctx.author.name}, não consegui me desconectar do canal @{channel}"


async def add_channels(bot):
    last = await bot.db.select1(
        "channels", what="timestamp", order_by="timestamp desc"
    )
    while True:
        channels = await bot.db.select_all(
            "channels",
            what=["name", "timestamp"],
            where={("timestamp", ">"): last},
            order_by="timestamp asc",
        )

        for channel in channels:
            if channel["name"] in bot.channels:
                # if it was joined using the %join command
                continue

            name = channel["name"]
            timestamp = channel["timestamp"]
            try:
                await bot.join_channels([name])
                bot.channels[name] = Channel()
                channel = bot.get_channel(name)
                await channel.send(f"@{name}, 👍")
                bot.log.info(f"Joined to {name}'s channel")
            except Exception as err:
                bot.log.error(
                    f"Failed to join to {name}'s channel\n{convert.traceback(err)}"
                )
            finally:
                last = timestamp

        await asyncio.sleep(60, loop=bot.loop)


def prepare(bot):
    bot.add_cog(Owner(bot))
    bot.loop.create_task(add_channels(bot))


def breakdown(bot):
    pass
