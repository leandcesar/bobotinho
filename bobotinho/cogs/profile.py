# -*- coding: utf-8 -*-
from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Bucket, Cog, Context, cooldown, command, helper, usage


class Profile(Cog):
    def __init__(self, bot: Bobotinho) -> None:
        self.bot = bot

    @helper("defina sua badge de apoiador")
    @usage("digite o comando e um emoji que quiser usar como badge")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["setbadge"])
    async def savebadge(self, ctx: Context, *, emoji: str = "") -> None:
        # TODO: %savebadge
        raise NotImplementedError()

    @helper("defina sua cidade para facilitar a consulta da sua previsão do tempo")
    @usage("digite o comando e o nome da sua cidade para agilizar a previsão do tempo")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["setcity"])
    async def savecity(self, ctx: Context, *, content: str = "") -> None:
        # TODO: %savecity
        raise NotImplementedError()

    @helper("salve um código hexadecimal de cor")
    @usage("digite o comando e o nome da sua cidade para agilizar a previsão do tempo")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["setcolor"])
    async def savecolor(self, ctx: Context, *, content: str = "") -> None:
        # TODO: %savecolor
        raise NotImplementedError()

    @helper("permita que utilizem comandos direcionados a você novamente")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command()
    async def mention(self, ctx: Context) -> None:
        ctx.user.update_settings(mention=True)
        return await ctx.reply(f"agora será possível usar comandos direcionados a você novamente")

    @helper("impeça que utilizem comandos direcionados a você")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command()
    async def unmention(self, ctx: Context) -> None:
        ctx.user.update_settings(mention=False)
        return await ctx.reply(f"não será mais possível usar comandos direcionados a você")


def prepare(bot: Bobotinho) -> None:
    bot.add_cog(Profile(bot))
