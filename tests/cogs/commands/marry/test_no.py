# -*- coding: utf-8 -*-
import pytest

from bobotinho.cogs.marry.commands import no


@pytest.mark.asyncio
async def test_no_but_you_has_no_a_pending_marriage_proposal(ctx):
    await no.command(ctx)
    assert ctx.response == "não há nenhum pedido de casamento para você"


@pytest.mark.asyncio
async def test_no(ctx):
    ctx.bot.cache["marry-user"] = "someone"
    await no.command(ctx)
    assert ctx.response == "você recusou o pedido de casamento de @someone 💔"
