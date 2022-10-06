# -*- coding: utf-8 -*-
from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Cog, Context, cooldown, command, helper, usage
from bobotinho.models.user import UserModel


class Profile(Cog):
    def __init__(self, bot: Bobotinho) -> None:
        self.bot = bot

    @helper("defina sua badge de apoiador")
    @usage("digite o comando e um emoji que quiser usar como badge")
    @cooldown(rate=3, per=10)
    @command(aliases=["setbadge"])
    async def savebadge(self, ctx: Context, *, emoji: str = "") -> None:
        # TODO: %savebadge
        raise NotImplementedError()

    @helper("defina sua cidade para facilitar a consulta da sua previsão do tempo")
    @usage("digite o comando e o nome da sua cidade para agilizar a previsão do tempo")
    @cooldown(rate=3, per=10)
    @command(aliases=["setcity"])
    async def savecity(self, ctx: Context, *, content: str = "") -> None:
        # TODO: %savecity
        raise NotImplementedError()

    @helper("salve um código hexadecimal de cor")
    @usage("digite o comando e o nome da sua cidade para agilizar a previsão do tempo")
    @cooldown(rate=3, per=10)
    @command(aliases=["setcolor"])
    async def savecolor(self, ctx: Context, *, content: str = "") -> None:
        # TODO: %savecolor
        raise NotImplementedError()


def prepare(bot: Bobotinho) -> None:
    bot.add_cog(Profile(bot))
