# -*- coding: utf-8 -*-
import pytest

from bobotinho.cogs.fun.commands import jokenpo


@pytest.mark.asyncio
async def test_jokenpo_raises_without_arg(ctx):
    with pytest.raises(TypeError):
        await jokenpo.command(ctx)


@pytest.mark.asyncio
async def test_jokenpo_invalid_arg(ctx):
    await jokenpo.command(ctx, "invalid")
    assert ctx.response is None


@pytest.mark.asyncio
async def test_jokenpo_with_rock(ctx):
    await jokenpo.command(ctx, "pedra")
    assert ctx.response == "eu escolhi tesoura, você deu sorte dessa vez"


@pytest.mark.asyncio
async def test_jokenpo_with_paper(ctx):
    await jokenpo.command(ctx, "papel")
    assert ctx.response == "eu também escolhi papel, nós empatamos..."


@pytest.mark.asyncio
async def test_jokenpo_with_scissors(ctx):
    await jokenpo.command(ctx, "tesoura")
    assert ctx.response == "eu escolhi pedra e consegui te prever facilmente"


@pytest.mark.asyncio
async def test_jokenpo_with_rock_emoji(ctx):
    await jokenpo.command(ctx, "✊")
    assert ctx.response == "eu escolhi papel e consegui te prever facilmente"


@pytest.mark.asyncio
async def test_jokenpo_with_paper_emoji(ctx):
    await jokenpo.command(ctx, "✋")
    assert ctx.response == "eu escolhi pedra, você deu sorte dessa vez"


@pytest.mark.asyncio
async def test_jokenpo_with_scissors_emoji(ctx):
    await jokenpo.command(ctx, "✌️")
    assert ctx.response == "eu escolhi pedra e consegui te prever facilmente"
