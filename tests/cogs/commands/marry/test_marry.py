# -*- coding: utf-8 -*-
import pytest
from unittest.mock import AsyncMock, patch

from bobotinho.cogs.marry.commands import marry


@pytest.mark.asyncio
async def test_marry_raises_without_arg(ctx):
    with pytest.raises(TypeError):
        await marry.command(ctx)


@pytest.mark.asyncio
async def test_marry_to_bot(ctx):
    await marry.command(ctx, "@bobotinho")
    assert ctx.response == "não fui programado para fazer parte de um relacionamento"


@pytest.mark.asyncio
async def test_marry_to_yourself(ctx):
    await marry.command(ctx, "@user")
    assert ctx.response == "você não pode se casar com você mesmo..."


@pytest.mark.asyncio
async def test_marry_but_you_have_a_pending_marriage_proposal(ctx):
    ctx.bot.cache["marry-user"] = "another"
    await marry.command(ctx, "@someone")
    assert ctx.response == 'antes você precisa responder ao pedido de @another! Digite "%yes" ou "%no"'


@pytest.mark.asyncio
async def test_marry_but_someone_has_a_pending_marriage_proposal(ctx):
    ctx.bot.cache["marry-someone"] = "another"
    await marry.command(ctx, "@someone")
    assert ctx.response == "@another chegou primeiro e já fez uma proposta à mão de @someone"


@pytest.mark.asyncio
@patch("bobotinho.database.models.wedding.Wedding.find_all", AsyncMock(side_effect=[[1]]))
async def test_marry_but_you_are_already_married_and_not_a_sponsor(ctx):
    await marry.command(ctx, "@someone")
    assert ctx.response == "traição é inaceitável, ao menos se divorcie antes de partir pra outra"


@pytest.mark.asyncio
@patch("bobotinho.database.models.wedding.Wedding.find_all", AsyncMock(side_effect=[[1, 2]]))
async def test_marry_but_you_are_already_married_to_two_users(ctx):
    ctx.user.sponsor = True
    await marry.command(ctx, "@someone")
    assert ctx.response == "você já está em dois relacionamentos, não é o suficiente?"


@pytest.mark.asyncio
async def test_marry_but_he_is_not_registered(ctx):
    await marry.command(ctx, "@someone")
    assert ctx.response == "@someone ainda não foi registrado (não usou nenhum comando)"


@pytest.mark.asyncio
@patch("bobotinho.database.models.user.User.get_or_none", AsyncMock(side_effect=[AsyncMock(mention=False)]))
async def test_marry_but_cannot_be_mentioned(ctx):
    await marry.command(ctx, "@someone")
    assert ctx.response == "esse usuário optou por não permitir mencioná-lo"


@pytest.mark.asyncio
@patch("bobotinho.database.models.wedding.Wedding.find", AsyncMock(side_effect=[True]))
@patch("bobotinho.database.models.wedding.Wedding.find_all", AsyncMock(side_effect=[[1], [1]]))
@patch("bobotinho.database.models.user.User.get_or_none", AsyncMock(side_effect=[AsyncMock()]))
async def test_marry_but_they_are_already_married(ctx):
    ctx.user.sponsor = True
    await marry.command(ctx, "@someone")
    assert ctx.response == "vocês dois já são casados... não se lembra?"


@pytest.mark.asyncio
@patch("bobotinho.database.models.wedding.Wedding.find", AsyncMock(side_effect=[False]))
@patch("bobotinho.database.models.wedding.Wedding.find_all", AsyncMock(side_effect=[[], [1]]))
@patch("bobotinho.database.models.user.User.get_or_none", AsyncMock(side_effect=[AsyncMock(sponsor=False)]))
async def test_marry_but_he_is_already_married_and_not_a_sponsor(ctx):
    await marry.command(ctx, "@someone")
    assert ctx.response == "controle seu desejo por pessoas casadas, @someone já está em um compromisso"


@pytest.mark.asyncio
@patch("bobotinho.database.models.wedding.Wedding.find", AsyncMock(side_effect=[False]))
@patch("bobotinho.database.models.wedding.Wedding.find_all", AsyncMock(side_effect=[[], [1, 2]]))
@patch("bobotinho.database.models.user.User.get_or_none", AsyncMock(side_effect=[AsyncMock()]))
async def test_marry_but_he_is_already_married_to_two_users(ctx):
    await marry.command(ctx, "@someone")
    assert ctx.response == "@someone já está em dois compromissos, não há espaço para mais um..."


@pytest.mark.asyncio
@patch("bobotinho.database.models.wedding.Wedding.find", AsyncMock(side_effect=[False]))
@patch("bobotinho.database.models.cookie.Cookie.get_or_none", AsyncMock(side_effect=[AsyncMock(stocked=100)]))
@patch("bobotinho.database.models.wedding.Wedding.find_all", AsyncMock(side_effect=[[], []]))
@patch("bobotinho.database.models.user.User.get_or_none", AsyncMock(side_effect=[AsyncMock()]))
async def test_marry_to_someone(ctx):
    await marry.command(ctx, "@someone")
    assert ctx.response == 'você pediu a mão de @someone, o usuário deve digitar "%yes" ou "%no" 💐💍'


@pytest.mark.asyncio
@patch("bobotinho.database.models.wedding.Wedding.find", AsyncMock(side_effect=[False]))
@patch("bobotinho.database.models.cookie.Cookie.get_or_none", AsyncMock(side_effect=[AsyncMock(stocked=0)]))
@patch("bobotinho.database.models.wedding.Wedding.find_all", AsyncMock(side_effect=[[], []]))
@patch("bobotinho.database.models.user.User.get_or_none", AsyncMock(side_effect=[AsyncMock()]))
async def test_marry_but_you_dont_have_cookies(ctx):
    await marry.command(ctx, "@someone")
    assert ctx.response == 'para pagar a aliança e todo o casório, você deve ter 100 cookies estocados'
