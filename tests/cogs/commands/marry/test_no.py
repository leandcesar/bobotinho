# -*- coding: utf-8 -*-
import pytest

from bobotinho.cogs.commands.marry import no


@pytest.mark.asyncio
async def test_no_but_you_has_no_a_pending_marriage_proposal(ctx):
    await no.func(ctx)
    assert ctx.response == "não há nenhum pedido de casamento para você"


@pytest.mark.asyncio
async def test_no(ctx):
    ctx.bot.cache["marry-user"] = "someone"
    await no.func(ctx)
    assert ctx.response == "você recusou o pedido de casamento de @someone 💔"
