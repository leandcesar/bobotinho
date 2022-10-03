# -*- coding: utf-8 -*-
from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Cog, Context, cooldown, command, helper, usage
from bobotinho.models.user import UserModel


class Pet(Cog):
    def __init__(self, bot: Bobotinho) -> None:
        self.bot = bot

    @helper("veja os pets de alguém")
    @cooldown(rate=3, per=10)
    @command(aliases=["pets"])
    async def pet(self, ctx: Context, name: str = "") -> None:
        # TODO
        raise NotImplementedError()

    @helper("adquira um dos pets disponíveis na loja")
    @usage("digite o comando e um dos pets disponíveis na loja para adquirí-lo")
    @cooldown(rate=3, per=10)
    @command()
    async def petbuy(self, ctx: Context) -> None:
        # TODO
        raise NotImplementedError()

    @helper("dê um nome para o seu pet")
    @usage("digite o comando e o nome que desejar para seu pet")
    @cooldown(rate=3, per=10)
    @command()
    async def petname(self, ctx: Context) -> None:
        # TODO
        raise NotImplementedError()

    @helper("faça carinho nos seus pets")
    @cooldown(rate=3, per=10)
    @command()
    async def petpat(self, ctx: Context) -> None:
        # TODO
        raise NotImplementedError()

    @helper("devolva um pet em troca de parte da quantia que gastou")
    @usage("digite o comando e o nome ou espécie do pet que quer devolver")
    @cooldown(rate=3, per=10)
    @command()
    async def petsell(self, ctx: Context) -> None:
        # TODO
        raise NotImplementedError()

    @helper("veja os pets disponíveis para adquirir")
    @cooldown(rate=3, per=10)
    @command(aliases=["petlist"])
    async def petshop(self, ctx: Context) -> None:
        # TODO
        raise NotImplementedError()


def prepare(bot: Bobotinho) -> None:
    bot.add_cog(Pet(bot))
