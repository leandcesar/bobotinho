# -*- coding: utf-8 -*-
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from bobotinho.database.base import timezone
from bobotinho.database.models import Reminder, User
from bobotinho.utils import convert, timetools

aliases = ["remindme"]
description = "Deixe um lembrete para algum usuário"
usage = "digite o comando, o nome de alguém e uma mensagem para deixar um lembrete"
extra_checks = ["Check.allowed", "Check.banword"]


async def command(ctx, arg: str, *, content: str = ""):
    invoke_by = ctx.message.content.partition(" ")[0][len(ctx.prefix):].lower()
    if invoke_by == "remindme":
        content = f"{arg} {content}"
        name = ctx.author.name
    elif arg == "me":
        arg = ""
        name = ctx.author.name
    else:
        name = convert.str2name(arg)
    if arg.isdecimal() and (remind := await Reminder.filter(id=int(arg), from_user_id=ctx.author.id).first()):
        await remind.fetch_related("to_user")
        mention = "você" if remind.to_user.name == ctx.author.name else f"@{remind.to_user.name}"
        if remind.scheduled_for:
            timestamp = timetools.format(remind.scheduled_for)
            ctx.response = f"seu lembrete de ID {remind.id} é para {mention} em {timestamp}: {remind.content}"
        else:
            ctx.response = f"seu lembrete de ID {remind.id} é para {mention}: {remind.content}"
    elif (
        arg.lower() == "delete"
        and content.isdecimal()
        and (remind := await Reminder.filter(id=int(content), from_user_id=ctx.author.id).first())
    ):
        await remind.delete()
        ctx.response = f"seu lembrete de ID {remind.id} foi deletado"
    elif arg.isdecimal() or (arg.lower() == "delete" and content.isdecimal()):
        ctx.response = "você não possui nenhum lembrete com esse ID"
    elif arg.lower() == "delete":
        ctx.response = "você deve passar o ID do lembrete que quer deletar"
    elif name == ctx.bot.nick:
        ctx.response = "estou sempre aqui... não precisa me deixar lembretes"
    elif await Reminder.filter(from_user_id=ctx.author.id).count() > 7 * (3 * ctx.user.sponsor or 1):
        ctx.response = "já existem muitos lembretes seus pendentes..."
    elif not (user := await User.get_or_none(name=name)):
        ctx.response = f"@{name} ainda não foi registrado (não usou nenhum comando)"
    elif arg and not user.mention:
        ctx.response = "esse usuário optou por não permitir mencioná-lo"
    elif await Reminder.filter(from_user_id=user.id, scheduled_for__isnull=True).count() > 7 * (3 * user.sponsor or 1):
        ctx.response = f"já existem muitos lembretes pendentes para @{name}"
    elif not content:
        ctx.response = "deixe alguma mensagem no lembrete"
    elif len(content) > 400:
        ctx.response = "essa mensagem é muito comprida"
    elif content.startswith("in ") and (match := timetools.find_relative_time(content[3:])):
        match_dict = match.groupdict()
        match_dict = {k: int(v) if v else 0 for k, v in match_dict.items()}
        content = content[3:].replace(match.group(0), "")
        try:
            scheduled_for = timezone.now() + relativedelta(**match_dict)
        except Exception:
            ctx.response = "isso ultrapassa o tempo máximo para lembretes cronometrados"
        else:
            remind = Reminder(
                from_user_id=ctx.author.id,
                to_user_id=user.id,
                channel_id=ctx.bot.channels[ctx.channel.name]["id"],
                content=content,
                scheduled_for=scheduled_for,
            )
            if remind.scheduled_to.total_seconds() < 0:
                ctx.response = "eu ainda não inventei a máquina do tempo"
            elif remind.scheduled_to.total_seconds() < 59:
                ctx.response = "o tempo mínimo para lembretes cronometrados é 1 minuto"
            else:
                await remind.save()
                mention = "você" if name == ctx.author.name else f"@{name}"
                timeago = timetools.date_in_full(remind.scheduled_to)
                ctx.response = f"{mention} será lembrado disso daqui {timeago} ⏲️ (ID {remind.id})"
    elif content.startswith(("on ", "at ")) and (match := timetools.find_absolute_time(content[3:])):
        match_dict = match.groupdict()
        match_dict = {
            k: int(v)
            if v
            else getattr(timezone.now(), k)
            for k, v in match_dict.items()
        }
        content = content[3:].replace(match.group(0), "")
        try:
            scheduled_for = timezone.now() + relativedelta(**match_dict) + timedelta(hours=3)  # time zones suck
        except Exception:
            ctx.response = "essa não é uma data válida"
        else:
            remind = Reminder(
                from_user_id=ctx.author.id,
                to_user_id=user.id,
                channel_id=ctx.bot.channels[ctx.channel.name]["id"],
                content=content,
                scheduled_for=scheduled_for,
            )
            if remind.scheduled_to.total_seconds() < 0:
                ctx.response = "eu ainda não inventei a máquina do tempo"
            elif remind.scheduled_to.total_seconds() < 59:
                ctx.response = "o tempo mínimo para lembretes cronometrados é 1 minuto"
            else:
                await remind.save()
                mention = "você" if name == ctx.author.name else f"@{name}"
                timestamp = timetools.format(remind.scheduled_for)
                ctx.response = f"{mention} será lembrado disso em {timestamp} 📅 (ID {remind.id})"
    else:
        remind = await Reminder.create(
            from_user_id=ctx.author.id,
            to_user_id=user.id,
            channel_id=ctx.bot.channels[ctx.channel.name]["id"],
            content=content,
        )
        mention = "você" if name == ctx.author.name else f"@{name}"
        ctx.response = f"{mention} será lembrado disso na próxima vez que falar no chat 📝 (ID {remind.id})"
