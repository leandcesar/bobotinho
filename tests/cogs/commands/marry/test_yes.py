# -*- coding: utf-8 -*-
import pytest
from unittest.mock import AsyncMock, patch

from bobotinho.cogs.commands.marry import yes


@pytest.mark.asyncio
async def test_yes_but_you_has_no_a_pending_marriage_proposal(ctx):
    await yes.func(ctx)
    assert ctx.response == "não há nenhum pedido de casamento para você"


@pytest.mark.asyncio
@patch("bobotinho.database.models.cookie.Cookie.get", AsyncMock(side_effect=[AsyncMock(stocked=0)]))
async def test_yes_but_someone_consumed_the_cookies(ctx):
    ctx.bot.cache["marry-user"] = "someone"
    await yes.func(ctx)
    assert ctx.response == (
        "parece que @someone gastou todos os cookies "
        "que eram pra aliança... o casamento precisou ser cancelado"
    )


@pytest.mark.asyncio
@patch("bobotinho.database.models.wedding.Wedding.create", AsyncMock())
@patch("bobotinho.database.models.cookie.Cookie.get", AsyncMock(side_effect=[AsyncMock(stocked=100)]))
async def test_yes(ctx):
    ctx.bot.cache["marry-user"] = "someone"
    await yes.func(ctx)
    assert ctx.response == "você aceitou o pedido de @someone, felicidades para o casal! 🎉💞"
