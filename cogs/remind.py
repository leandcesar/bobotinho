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

import aiohttp
import asyncio
import config
import datetime
import re

from dateutil.relativedelta import relativedelta
from ext.command import command
from twitchio.ext import commands
from utils import asyncrq, convert, checks


class Remind(commands.AutoCog):
    def __init__(self, bot):
        self.bot = bot

    def _prepare(self, bot):
        pass

    pattern_in = re.compile(
        r"""(?P<in>\b(?:in|daqui))\s
            (\b(?P<years>\d+)\s?(?:years|year|y|anos|ano|a)\b\s?)?
            (\b(?P<months>\d+)\s?(?:months|month|meses|mês|mes)\b\s?)?
            (\b(?P<weeks>\d+)\s?(?:weeks|week|w|semanas|semana)\b\s?)?
            (\b(?P<days>\d+)\s?(?:days|day|dias|dia|d)\b\s?)?
            (\b(?P<hours>\d+)\s?(?:hours|hour|horas|hora|h)\b\s?)?
            (\b(?P<minutes>\d+)\s?(?:minutes|minute|minutos|minuto|min|m)\b\s?)?
            (\b(?P<seconds>\d+)\s?(?:seconds|second|sec|segundos|segundo|seg|s)\b\s?)?""",
        re.VERBOSE,
    )

    pattern_on = re.compile(
        r"""(?P<on>\b(?:on|em))\s
            (?:\b
                (?P<hour>[01]?[0-9]|2[0-3])
                (?:h|:(?P<minute>[0-5][0-9])
                (?::(?P<second>[0-5][0-9]))?
            )\b\s?)?
            (?:\b
                (?P<day>0?[1-9]|[12][0-9]|3[01])[\/-]
                (?P<month>0?[1-9]|1[012])
                (?:[\/-](?P<year>[0-9]{4}))?
            \b\s?)?""",
        re.VERBOSE,
    )

    @command(
        aliases=["remindme"],
        description="deixe um lembrete para algum usuário",
        usage="digite o comando, o nome de alguém e uma mensagem para deixar um lembrete",
    )
    async def remind(self, ctx, user: str, *, message: str = ""):
        if ctx.command.invoked_by == "remindme":
            if user:
                message = user + " " + message
            user = ctx.author.name
        elif user == "me":
            user = ctx.author.name
        else:
            user = convert.user(user)

        if not user or not message:
            return
        elif user == self.bot.nick:
            ctx.response = f"@{ctx.author.name}, estou sempre aqui... não precisa me deixar lembretes"
        elif await self.bot.db.count("reminds", where={"name": ctx.author.name}) > 15:
            ctx.response = f"@{ctx.author.name}, já existem muitos lembretes seus pendentes..."
        elif not await self.bot.db.exists("users", where={"name": user}):
            ctx.response = (
                f"@{ctx.author.name}, @{user} ainda não foi registrado "
                f"(o usuário precisa ter usado algum comando)"
            )
        elif len(message) > 300:
            ctx.response = f"@{ctx.author.name}, essa mensagem é muito comprida"
        elif not checks.is_allowed(ctx) and checks.is_link(message):
            ctx.response = f"@{ctx.author.name}, apenas inscritos, vips e moderadores podem enviar links"
        elif await self.bot.db.count("reminds", where={"name": user}) > 15:
            ctx.response = f"@{ctx.author.name}, já existem muitos lembretes pendentes para @{user}"
        elif user == "noblezito" and ("betterttv.com" in message or "frankerfacez.com" in message):
            ctx.response = f"@{ctx.author.name}, não."
        else:
            match = self.pattern_in.search(message)
            if (
                match
                and match.group("in")
                and any([match.groups()[1:]])
                and message.startswith(match.group(0))
            ):
                match_dict = match.groupdict()
                _ = match_dict.pop("in")
                for k, v in match_dict.items():
                    match_dict[k] = int(v) if v else 0
                timer = relativedelta(**match_dict)
                try:
                    timestamp = convert.date(timer)
                    timesince = convert.timesince(timestamp, future=True)
                except OverflowError:
                    ctx.response = f"@{ctx.author.name}, isso ultrapassa o tempo máximo para lembretes cronometrados"
                except Exception as err:
                    raise err
                else:
                    if timestamp - datetime.datetime.utcnow() < datetime.timedelta(seconds=59):
                        ctx.response = f"@{ctx.author.name}, o tempo mínimo para lembretes cronometrados é 1 minuto"
                    else:
                        await self.bot.db.insert(
                            "reminds",
                            values={
                                "name": ctx.author.name,
                                "channel": ctx.channel.name,
                                "message": message.replace(match.group(0), ""),
                                "timestamp": ctx.message.timestamp,
                                "to_name": user,
                                "to_timestamp": timestamp,
                            },
                        )
                        user = "você" if user == ctx.author.name else f"@{user}"
                        ctx.response = f"@{ctx.author.name}, {user} será lembrado disso daqui {timesince} ⏲"
                return
            match = self.pattern_on.search(message)
            if (
                match
                and match.group("on")
                and any([match.groups()[1:]])
                and message.startswith(match.group(0))
            ):
                match_dict = match.groupdict()
                _ = match_dict.pop("on")
                now = datetime.datetime.utcnow()
                match_dict = {
                    k: int(v) 
                    if v else getattr(now, k)
                    for k, v in match_dict.items()
                }
                try:
                    timestamp = datetime.datetime(**match_dict)
                except ValueError:
                    ctx.response = f"@{ctx.author.name}, essa não é uma data válida"
                except Exception as err:
                    raise err
                else:
                    if timestamp + datetime.timedelta(hours=3) < now:
                        ctx.response = f"@{ctx.author.name}, eu ainda não inventei a máquina do tempo"
                    elif timestamp + datetime.timedelta(hours=3) < now + datetime.timedelta(seconds=60):
                        ctx.response = f"@{ctx.author.name}, o tempo mínimo para lembretes cronometrados é 1 minuto"
                    else:
                        await self.bot.db.insert(
                            "reminds",
                            values={
                                "name": ctx.author.name,
                                "channel": ctx.channel.name,
                                "message": message.replace(match.group(0), ""),
                                "timestamp": ctx.message.timestamp,
                                "to_name": user,
                                "to_timestamp": timestamp + datetime.timedelta(hours=3),
                            },
                        )
                        user = "você" if user == ctx.author.name else f"@{user}"
                        timestamp = timestamp.strftime("%d/%m/%Y às %H:%M:%S")
                        ctx.response = f"@{ctx.author.name}, {user} será lembrado disso em {timestamp} ⏲"
                return
            if await self.bot.db.exists("reminds", where={"name": ctx.author.name, "to_name": user, "message": message}):
                ctx.response = f"@{ctx.author.name}, você já deixou esse lembrete para @{user}"
            else:
                await self.bot.db.insert(
                    "reminds",
                    values={
                        "name": ctx.author.name,
                        "channel": ctx.channel.name,
                        "message": message,
                        "timestamp": ctx.message.timestamp,
                        "to_name": user,
                    },
                )
                user = "você" if user == ctx.author.name else f"@{user}"
                ctx.response = f"@{ctx.author.name}, {user} será lembrado disso na próxima vez que falar no chat 📝"

async def timed_reminder(bot):
    while True:
        now = datetime.datetime.utcnow()
        row = await bot.db.select(
            "reminds", 
            where={("to_timestamp", "<="): now + datetime.timedelta(seconds=60)},
            order_by="to_timestamp asc",
        )
        
        if (
            row
            and bot.channels.is_online(row["channel"])
            and not bot.channels.is_disabled(row["channel"], "remind")
        ):
            user = "você" if row["name"] == row["to_name"] else f'@{row["name"]}'
            if now <= row["to_timestamp"]:
                delta = row["to_timestamp"] - now
                await asyncio.sleep(delta.total_seconds(), loop=bot.loop)
            timesince = convert.timesince(row["timestamp"], future=False)
            if row["message"]:
                response = f'@{row["to_name"]}, {user} deixou um lembrete cronometrado: {row["message"]} ({timesince})'
            else:
                response = f'@{row["to_name"]}, {user} deixou um lembrete cronometrado ({timesince})'
            await bot.db.delete("reminds", where={"id": row["id"]})
            if not bot.channels.is_banword(row["channel"], response):
                try:
                    await bot.get_channel(row["channel"]).send(response)
                    bot.log.info(f'#{row["channel"]} > {response}')
                except Exception as err:
                    bot.log.error(f'{row["channel"]}\n{convert.traceback(err)}')
        elif row:
            await bot.db.update(
                "reminds", 
                values={"to_timestamp": row["timestamp"] + datetime.timedelta(seconds=3600)}, 
                where={"id": row["id"]},
            )
        else:
            await asyncio.sleep(60, loop=bot.loop)

async def reminder(bot, message):
    if bot.channels.is_disabled(message.channel.name, "remind"):
        return

    rows = await bot.db.select_all(
        "reminds", where={"to_name": message.author.name}, order_by="timestamp asc",
    )
    if not rows:
        return
    
    for row in rows:
        if row["to_timestamp"]:
            continue
        # merge all reminds in one message...
        timesince = convert.timesince(row["timestamp"])
        if row["name"] == message.author.name:
            response = f'@{message.author.name}, lembrete de você mesmo: {row["message"]} ({timesince})'
        else:
            response = f'@{message.author.name}, @{row["name"]} deixou um lembrete: {row["message"]} ({timesince})'
        if bot.channels.is_banword(message.channel.name, response):
            continue
        await bot.db.delete("reminds", where={"id": row["id"]})
        await message.channel.send(response)
        bot.log.info(
            f"#{message.channel.name} {message.author.name}: {message.content} > {response}"
        )
        return True


def prepare(bot):
    bot.add_cog(Remind(bot))
    bot.loop.create_task(timed_reminder(bot))


def breakdown(bot):
    pass
