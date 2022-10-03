# -*- coding: utf-8 -*-
from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Cog, Context, cooldown, command, helper, usage
from bobotinho.models.user import UserModel


class Marry(Cog):
    def __init__(self, bot: Bobotinho) -> None:
        self.bot = bot

    @helper("divorcie-se da pessoa com quem você é casada")
    @usage("digite o comando e o nome da pessoa com quem se casou para se divorciar")
    @cooldown(rate=3, per=10)
    @command()
    async def divorce(self, ctx: Context, name: str) -> None:
        # TODO
        raise NotImplementedError()

    @helper("saiba há quanto tempo algum usuário está casado")
    @cooldown(rate=3, per=10)
    @command(aliases=["ma", "married"])
    async def marriage(self, ctx: Context, name: str = "") -> None:
        # TODO
        raise NotImplementedError()

    @helper("case-se e seja feliz para sempre, mas isso custará cookies")
    @usage("digite o comando e o nome de quem você quer pedir em casamento")
    @cooldown(rate=3, per=10)
    @command()
    async def marry(self, ctx: Context, name: str = "") -> None:
        # TODO
        raise NotImplementedError()


def prepare(bot: Bobotinho) -> None:
    bot.add_cog(Marry(bot))
