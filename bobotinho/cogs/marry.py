# -*- coding: utf-8 -*-
from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Bucket, Cog, Context, cooldown, command, helper, usage
from bobotinho.utils.time import timeago


class Marry(Cog):
    def __init__(self, bot: Bobotinho) -> None:
        self.bot = bot
        self.proposals = {}

    async def cog_check(self, ctx: Context) -> bool:
        if ctx.args and isinstance(ctx.args[0], str):
            ctx.args[0] = ctx.args[0].lstrip("@").rstrip(",").lower()
        return True

    @helper("divorcie-se da pessoa com quem você é casada")
    @usage("digite o comando e o nome da pessoa com quem se casou para se divorciar")
    @cooldown(rate=1, per=10, bucket=Bucket.member)
    @command()
    async def divorce(self, ctx: Context, name: str) -> None:
        if name == self.bot.nick:
            return await ctx.reply("eu nunca estaria casado com você")
        elif name == ctx.author.name:
            return await ctx.reply("você não pode se livrar de você mesmo")
        elif ctx.user.single:
            return await ctx.reply("você não está casado com ninguém...")
        else:
            user = await self.bot.fetch_user_db(name)
            if not user:
                return await ctx.reply(f"@{name} ainda não foi registrado (não usou nenhum comando)")

        for wedding in ctx.user.weddings:
            if wedding.user_id == user.id:
                ctx.user.divorce(user_id=user.id)
                user.divorce(user_id=ctx.author.id)
                return await ctx.reply("então, é isso... da próxima vez, case-se com alguém que você realmente ame, e não qualquer um por aí")
        else:
            return await ctx.reply("você não sabe nem o nome da pessoa com quem está casado?")

    @helper("saiba há quanto tempo algum usuário está casado")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["ma", "married"])
    async def marriage(self, ctx: Context, name: str = "") -> None:
        name = name or ctx.author.name
        if name == self.bot.nick:
            return await ctx.reply("nunca me casarei com ninguém")
        if name == ctx.author.name:
            user = ctx.user
        else:
            user = await self.bot.fetch_user_db(name)
            if not user:
                return await ctx.reply(f"@{name} ainda não foi registrado (não usou nenhum comando)")
        if user.settings and not user.settings.mention:
            return await ctx.reply("esse usuário optou por não permitir ser mencionado")
        mention = "você" if name == ctx.author.name else f"@{name}"
        if not user.weddings:
            return await ctx.reply(f"{mention} não está casado com ninguém")

        twitch_users = [await self.bot.fetch_user(id=wedding.user_id) for wedding in user.weddings]
        weddings = [
            f'@{twitch_user.name} desde {wedding.created_on.strftime("%d/%m/%Y")} (há {timeago(wedding.created_on).humanize(short=True)})'
            for twitch_user, wedding in zip(twitch_users, user.weddings)
            if not wedding.divorced
        ]
        wedding = " e com ".join(weddings)
        return await ctx.reply(f"{mention} está casado com {wedding}")

    @helper("case-se e seja feliz para sempre, mas isso custará cookies")
    @usage("digite o comando e o nome de quem você quer pedir em casamento")
    @cooldown(rate=1, per=10, bucket=Bucket.member)
    @command()
    async def marry(self, ctx: Context, name: str) -> None:
        if name == self.bot.nick:
            return await ctx.reply("não fui programado para fazer parte de um relacionamento")
        elif name == ctx.author.name:
            return await ctx.reply("você não pode se casar com você mesmo...")
        else:
            user = await self.bot.fetch_user_db(name)
            if not user:
                return await ctx.reply(f"@{name} ainda não foi registrado (não usou nenhum comando)")

        if user.settings and not user.settings.mention:
            return await ctx.reply("esse usuário optou por não permitir ser mencionado")
        elif name in self.proposals:
            return await ctx.reply(f"@{self.proposals[name]} chegou primeiro e já fez uma proposta à mão de @{name}, aguarde pela resposta")
        elif not ctx.user.single and user.id in [wedding.user_id for wedding in ctx.user.weddings]:
            return await ctx.reply("vocês dois já são casados... não se lembra?")
        elif not ctx.user.single:
            return await ctx.reply(f"traição é inaceitável, ao menos se divorcie antes de partir pra outra")
        elif not user.single:
            return await ctx.reply(f"controle seu desejo por pessoas casadas, @{user.name} já está em um compromisso")
        elif not ctx.user.cookies or ctx.user.cookies.stocked < 100:
            return await ctx.reply(f"para pagar a aliança e todo o casório, você precisa de 100 cookies estocados")

        try:
            self.proposals[name] = ctx.author.name
            check = lambda message: (
                message.author
                and message.author.name == name
                and message.channel.name == ctx.channel.name
                and message.content.lower() in ("sim", "s", "não", "nao", "n")
            )
            await ctx.reply(f"você pediu a mão de @{name}! @{name}, você aceita? 💐💍 (sim/não)")
            response = await self.bot.wait_for("message", check, timeout=60)
            message = response[0]
            if message.content.lower() in ("sim", "s"):
                ctx.user.refresh()
                if ctx.user.cookies.stocked < 100:
                    return await ctx.send(f"parece que @{ctx.author.name} gastou todos os cookies que eram pra aliança... o casamento precisou ser cancelado")
                ctx.user.update_cookie(consume=100)
                ctx.user.marry(user_id=user.id)
                user.marry(user_id=ctx.user.id)
                await ctx.send(f"@{user.name} aceitou o pedido de casamento de @{name}, felicidades para o casal! 🎉💞")
            elif message.content.lower() in ("não", "nao", "n"):
                await ctx.send(f"@{name} recusou o pedido de casamento de @{ctx.author.name} 💔")
        except Exception:
            await ctx.reply(f"@{name} não respondeu ao seu pedido a tempo 💔")
        finally:
            self.proposals.pop(name)


def prepare(bot: Bobotinho) -> None:
    bot.add_cog(Marry(bot))
