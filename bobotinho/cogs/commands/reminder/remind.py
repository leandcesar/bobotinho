# -*- coding: utf-8 -*-
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from bobotinho.utils import checks, convert, timetools
from bobotinho.database import models

aliases = ["remindme"]
description = "Deixe um lembrete para algum usuário"
usage = "digite o comando, o nome de alguém e uma mensagem para deixar um lembrete"
extra_checks = [checks.is_allowed, checks.is_banword]


async def func(ctx, arg: str, *, content: str = ""):
    if ctx.command.invocation == "remindme":
        content = f"{arg} {content}"
        name = ctx.author.name
    elif arg == "me":
        name = ctx.author.name
    else:
        name = convert.str2username(arg)
    if not name:
        ctx.response = "nome de usuário inválido"
    elif name == ctx.bot.nick:
        ctx.response = "estou sempre aqui... não precisa me deixar lembretes"
    elif await models.Reminder.filter(from_user_id=ctx.author.id).count() > 7:
        ctx.response = "já existem muitos lembretes seus pendentes..."
    elif not (user := await models.User.get_or_none(name=name)):
        ctx.response = f"@{name} ainda não foi registrado (não usou nenhum comando)"
    elif await models.Reminder.filter(from_user_id=user.id).count() > 7:
        ctx.response = f"já existem muitos lembretes pendentes para @{name}"
    elif len(content) > 400:
        ctx.response = "essa mensagem é muito comprida"
    elif match := timetools.find_relative_time(content):
        match_dict = match.groupdict()
        match_dict = {k: int(v) if v else 0 for k, v in match_dict.items()}
        content = content.replace(match.group(0), "")
        try:
            scheduled_for = ctx.message.timestamp + relativedelta(**match_dict)
        except Exception:
            ctx.response = "isso ultrapassa o tempo máximo para lembretes cronometrados"
        else:
            if (scheduled_for - ctx.message.timestamp).total_seconds() < 60:
                ctx.response = "o tempo mínimo para lembretes cronometrados é 1 minuto"
            else:
                await models.Reminder.create(
                    from_user_id=ctx.author.id,
                    to_user_id=user.id,
                    channel_id=ctx.bot.channels[ctx.channel.name]["id"],
                    content=content,
                    scheduled_for=scheduled_for,
                )
                mention = "você" if name == ctx.author.name else f"@{name}"
                timeago = timetools.timeago(ctx.message.timestamp, now=scheduled_for)
                ctx.response = f"{mention} será lembrado disso daqui {timeago} ⏲️"
    elif match := timetools.find_absolute_time(content):
        match_dict = match.groupdict()
        match_dict = {
            k: int(v)
            if v
            else getattr(ctx.message.timestamp, k)
            for k, v in match_dict.items()
        }
        content = content.replace(match.group(0), "")
        try:
            scheduled_for = ctx.message.timestamp + relativedelta(**match_dict) + timedelta(hours=3)
        except Exception:
            ctx.response = "essa não é uma data válida"
        else:
            if scheduled_for <= ctx.message.timestamp:
                ctx.response = "eu ainda não inventei a máquina do tempo"
            elif (scheduled_for - ctx.message.timestamp).total_seconds() < 60:
                ctx.response = "o tempo mínimo para lembretes cronometrados é 1 minuto"
            else:
                await models.Reminder.create(
                    from_user_id=ctx.author.id,
                    to_user_id=user.id,
                    channel_id=ctx.bot.channels[ctx.channel.name]["id"],
                    content=content,
                    scheduled_for=scheduled_for,
                )
                mention = "você" if name == ctx.author.name else f"@{name}"
                timestamp = (scheduled_for - timedelta(hours=3)).strftime("%d/%m/%Y às %H:%M:%S")
                ctx.response = f"{mention} será lembrado disso em {timestamp} 📅"
    else:
        await models.Reminder.create(
            from_user_id=ctx.author.id,
            to_user_id=user.id,
            channel_id=ctx.bot.channels[ctx.channel.name]["id"],
            content=content,
        )
        mention = "você" if name == ctx.author.name else f"@{name}"
        ctx.response = f"{mention} será lembrado disso na próxima vez que falar no chat 📝"
