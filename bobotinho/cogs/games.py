# -*- coding: utf-8 -*-
from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Bucket, Cog, Context, cooldown, command, helper, usage


class Game(Cog):
    def __init__(self, bot: Bobotinho) -> None:
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        return ctx.author.is_mod or ctx.author.is_broadcaster

    @helper("jogo da forca, descubra a palavra em até 5 tentativas e 2 minutos")
    @cooldown(rate=1, per=15, bucket=Bucket.member)
    @command(aliases=["hm"])
    async def hangman(self, ctx: Context, *, content: str = "") -> None:
        # TODO: %hangman
        raise NotImplementedError()

    @helper("jogo da palavra mais comprida com determinada sílaba, dura 30 segundas")
    @cooldown(rate=1, per=15, bucket=Bucket.member)
    @command(aliases=["lw"])
    async def longestword(self, ctx: Context, *, content: str = "") -> None:
        # TODO: %longestword
        raise NotImplementedError()

    @helper("jogo de mais palavras com determinada sílaba, dura 30 segundas")
    @cooldown(rate=1, per=15, bucket=Bucket.member)
    @command(aliases=["mw"])
    async def mostword(self, ctx: Context, *, content: str = "") -> None:
        # TODO: %mostword
        raise NotImplementedError()


def prepare(bot: Bobotinho) -> None:
    bot.add_cog(Game(bot))
