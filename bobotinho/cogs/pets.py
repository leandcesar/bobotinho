# -*- coding: utf-8 -*-
from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Cog, Context, cooldown, command, helper, usage
from bobotinho.models.user import UserModel
from bobotinho.utils.convert import json2dict

PETS = json2dict("bobotinho//data//pets.json")


class Pet(Cog):
    def __init__(self, bot: Bobotinho) -> None:
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        if ctx.args and isinstance(ctx.args[0], str):
            ctx.args[0] = ctx.args[0].lstrip("@").rstrip(",").lower()
        return True

    @helper("veja os pets de alguém")
    @cooldown(rate=3, per=10)
    @command(aliases=["pets"])
    async def pet(self, ctx: Context, name: str = "") -> None:
        name = name or ctx.author.name
        if name == self.bot.nick:
            return await ctx.reply("eu tenho todos os pets, e ofereço alguns pra vocês")
        twitch_user = await self.bot.fetch_user(name)
        if not twitch_user:
            return await ctx.reply(f"@{name} é um usuário inválido")
        user = UserModel.get_or_none(twitch_user.id)
        if not user:
            return await ctx.reply(f"@{name} ainda não foi registrado (não usou nenhum comando)")
        mention = "você" if name == ctx.author.name else f"@{name}"
        if user.pets:
            pets = " ".join([f'{pet} {PETS[pet.specie]["emoji"]}' for pet in user.pets])
            return await ctx.reply(f"{mention} possui {pets}")
        return await ctx.reply(f"{mention} não possui nenhum pet")

    @helper("adquira um dos pets disponíveis na loja")
    @usage("digite o comando e um dos pets disponíveis na loja para adquirí-lo")
    @cooldown(rate=3, per=10)
    @command()
    async def petbuy(self, ctx: Context) -> None:
        # TODO: %petbuy
        raise NotImplementedError()

    @helper("dê um nome para o seu pet")
    @usage("digite o comando e o nome que desejar para seu pet")
    @cooldown(rate=3, per=10)
    @command()
    async def petname(self, ctx: Context) -> None:
        # TODO: %petname
        raise NotImplementedError()

    @helper("faça carinho nos seus pets")
    @cooldown(rate=3, per=10)
    @command()
    async def petpat(self, ctx: Context) -> None:
        # TODO: %petpat
        raise NotImplementedError()

    @helper("devolva um pet em troca de parte da quantia que gastou")
    @usage("digite o comando e o nome ou espécie do pet que quer devolver")
    @cooldown(rate=3, per=10)
    @command()
    async def petsell(self, ctx: Context) -> None:
        # TODO: %petsell
        raise NotImplementedError()

    @helper("veja os pets disponíveis para adquirir")
    @cooldown(rate=3, per=10)
    @command(aliases=["petlist"])
    async def petshop(self, ctx: Context) -> None:
        # TODO: %petshop
        raise NotImplementedError()


def prepare(bot: Bobotinho) -> None:
    bot.add_cog(Pet(bot))
