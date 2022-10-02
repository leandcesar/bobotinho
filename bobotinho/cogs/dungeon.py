# -*- coding: utf-8 -*-
from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Cog, Context, cooldown, command, helper, usage
from bobotinho.models.user import UserModel


class Dungeon(Cog):
    def __init__(self, bot: Bobotinho) -> None:
        self.bot = bot

    @helper("entre na dungeon, faça sua escolha e adquira experiência")
    @cooldown(rate=3, per=10)
    @command(aliases=["ed"])
    async def enterdungeon(self, ctx: Context, *, content: str = "") -> None:
        # TODO
        ...

    @helper("entre na dungeon e adquira experiência sem precisar tomar uma escolha")
    @cooldown(rate=3, per=10)
    @command(aliases=["fed", "fd"])
    async def fastdungeon(self, ctx: Context) -> None:
        # TODO
        ...

    @helper("veja qual o seu level (ou de alguém) e outras estatísticas da dungeon")
    @cooldown(rate=3, per=10)
    @command(aliases=["lvl"])
    async def level(self, ctx: Context, name: str = "") -> None:
        # TODO
        ...

    @helper("saiba quais são os melhores jogadores da dungeon")
    @cooldown(rate=3, per=10)
    @command()
    async def rank(self, ctx: Context, order_by: str = "") -> None:
        # TODO
        ...


def prepare(bot: Bobotinho) -> None:
    bot.add_cog(Dungeon(bot))
