# -*- coding: utf-8 -*-
from bobotinho.database.models import Reminder

description = "Veja os IDs dos lembretes que você deixou"


async def command(ctx):
    if reminds := await Reminder.filter(from_user_id=ctx.author.id).order_by("id").all():
        reminds_id = ", ".join([str(remind.id) for remind in reminds])
        ctx.response = f"seus lembretes pendentes são os de ID: {reminds_id}"
    else:
        ctx.response = "não tem nenhum lembrete seu pendente"
