# -*- coding: utf-8 -*-
from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Cog, Context, cooldown, command, helper, usage
from bobotinho.models.user import UserModel
from bobotinho.utils.time import timeago


class Marry(Cog):
    def __init__(self, bot: Bobotinho) -> None:
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        ctx.args[0] = ctx.args[0].lstrip("@").rstrip(",").lower()
        return True

    @helper("divorcie-se da pessoa com quem você é casada")
    @usage("digite o comando e o nome da pessoa com quem se casou para se divorciar")
    @cooldown(rate=3, per=10)
    @command()
    async def divorce(self, ctx: Context, name: str) -> None:
        # TODO: %divorce
        raise NotImplementedError()

    @helper("saiba há quanto tempo algum usuário está casado")
    @cooldown(rate=3, per=10)
    @command(aliases=["ma", "married"])
    async def marriage(self, ctx: Context, name: str = "") -> None:
        name = name or ctx.author.name
        if name == self.bot.nick:
            return await ctx.reply("nunca me casarei com ninguém")
        twitch_user = await self.bot.fetch_user(name)
        if not twitch_user:
            return await ctx.reply(f"@{name} é um usuário inválido")
        user = UserModel.get_or_none(twitch_user.id)
        if not user:
            return await ctx.reply(f"@{name} ainda não foi registrado (não usou nenhum comando)")
        mention = "você" if name == ctx.author.name else f"@{name}"
        if not user.weddings:
            return await ctx.reply(f"{mention} não está casado com ninguém")

        twitch_users = [await self.bot.fetch_user(id=wedding.user_id) for wedding in user.weddings]
        weddings = [
            f'@{twitch_user.name} desde {wedding.created_on.strftime("%d/%m/%Y")} (há {timeago(wedding.created_on).humanize(precision=2)})'
            for twitch_user, wedding in zip(twitch_users, user.weddings)
            if not wedding.divorced
        ]
        wedding = " e com ".join(weddings)
        return await ctx.reply(f"{mention} está casado com {wedding}")

    @helper("case-se e seja feliz para sempre, mas isso custará cookies")
    @usage("digite o comando e o nome de quem você quer pedir em casamento")
    @cooldown(rate=3, per=10)
    @command()
    async def marry(self, ctx: Context, name: str = "") -> None:
        # TODO: %marry
        raise NotImplementedError()


def prepare(bot: Bobotinho) -> None:
    bot.add_cog(Marry(bot))
