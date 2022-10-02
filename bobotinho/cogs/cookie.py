# -*- coding: utf-8 -*-
from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Cog, Context, cooldown, command, helper, usage
from bobotinho.models.user import UserModel
from bobotinho.utils.rand import random_line_from_txt, random_choices


class Cookie(Cog):
    def __init__(self, bot: Bobotinho) -> None:
        self.bot = bot

    @helper("coma um cookie e receba uma frase da sorte")
    @usage("digite o comando e a quantidade de cookies que quer comer (opcional)")
    @cooldown(rate=3, per=10)
    @command()
    async def cookie(self, ctx: Context, amount: int = 1) -> None:
        if amount == 0:
            return await ctx.reply("você não comeu nenhum cookie, uau!")
        if amount < 0:
            return await ctx.reply(f"para comer {amount} cookies, você antes precisa reverter a entropia")
        user = UserModel.get(ctx.author.id)
        if amount > 1 and user.update_cookie(eat=amount):
            return await ctx.reply(f"você comeu {amount} cookies de uma só vez 🥠")
        if amount > 1:
            return await ctx.reply(f"você não tem {amount} cookies estocados para comer")
        if amount == 1 and user.update_cookie(daily=True, eat=1):
            cookie = random_line_from_txt("bobotinho//data//cookies.txt")
            return await ctx.reply(f"{cookie} 🥠")
        return await ctx.reply("você já usou seu cookie diário, a próxima fornada sai às 6 da manhã! ⌛")

    @helper("veja quantos cookies alguém já comeu")
    @usage("digite o comando e a quantidade de cookies que quer comer (opcional)")
    @cooldown(rate=3, per=10)
    @command(aliases=["cc"])
    async def cookiecount(self, ctx: Context, name: str = "") -> None:
        name = name.lstrip("@").rstrip(",").lower() or ctx.author.name
        if name == self.bot.nick:
            return await ctx.reply("eu tenho cookies infinitos, e distribuo uma fração deles para vocês")
        user = UserModel.one(UserModel.name == name)
        if not user:
            return await ctx.reply(f"@{name} ainda não foi registrado (não usou nenhum comando)")
        mention = "você" if name == ctx.author.name else f"@{name}"
        if user.cookies:
            return await ctx.reply(
                f"{mention} já comeu {user.cookies.count} cookies, presenteou {user.cookies.donated}, "
                f"foi presenteado com {user.cookies.received} e tem {user.cookies.stocked} estocados"
            )
        return await ctx.reply(f"{mention} ainda não comeu nenhum cookie")

    @helper("presenteie alguém com seu cookie diário")
    @usage("digite o comando e o nome de alguém para presenteá-lo com seu cookie")
    @cooldown(rate=3, per=10)
    @command(aliases=["give"])
    async def gift(self, ctx: Context, name: str = "") -> None:
        name = name.lstrip("@").rstrip(",").lower() or ctx.author.name
        if name == self.bot.nick:
            return await ctx.reply("eu não quero seu cookie")
        if name == ctx.author.name:
            return await ctx.reply("você presenteou você mesmo, uau!")
        user_to = UserModel.one(UserModel.name == name)
        if not user_to:
            return await ctx.reply(f"@{name} ainda não foi registrado (não usou nenhum comando)")
        user_from = UserModel.get(ctx.author.id)
        if user_from.update_cookie(daily=True, donate=1):
            user_to.update_cookie(receive=1)
            return await ctx.reply(f"você presenteou @{name} com um cookie 🎁")
        return await ctx.reply("você já usou seu cookie diário, a próxima fornada sai às 6 da manhã! ⌛")

    @helper("aposte seu cookie diário para ter a chance de ganhar outros")
    @cooldown(rate=3, per=10)
    @command(aliases=["sm"])
    async def slotmachine(self, ctx: Context) -> None:
        user = UserModel.get(ctx.author.id)
        if user.update_cookie(daily=True):
            x, y, z = random_choices("🍇🍊🍋🍒🍉🍐", k=3)
            if x == y == z:
                user.update_cookie(earnings=10)
                return await ctx.reply(f"[{x}{y}{z}] você usou seu cookie diário e ganhou 10 cookies! PogChamp")
            elif x == y or x == z or y == z:
                user.update_cookie(earnings=3)
                return await ctx.reply(f"[{x}{y}{z}] você usou seu cookie diário e ganhou 3 cookies!")
            else:
                return await ctx.reply(f"[{x}{y}{z}] você perdeu seu cookie diário...")
        return await ctx.reply("você já usou seu cookie diário, a próxima fornada sai às 6 da manhã! ⌛")

    @helper("estoque o seu cookie diário, caso não queira usá-lo")
    @cooldown(rate=3, per=10)
    @command()
    async def stock(self, ctx: Context) -> None:
        user = UserModel.get(ctx.author.id)
        if user.update_cookie(daily=True):
            return await ctx.reply("você estocou seu cookie diário")
        return await ctx.reply("você já usou seu cookie diário, a próxima fornada sai às 6 da manhã! ⌛")

    @helper("veja quais são os maiores comedores ou doadores de cookies")
    @cooldown(rate=3, per=10)
    @command()
    async def top(self, ctx: Context, order_by: str = "count") -> None:
        if order_by in ["gift", "gifts", "give", "gives", "giver", "givers"]:
            attr, title = "donated", "givers"
        else:
            attr, title = "count", "cookiers"
        users = UserModel.all(UserModel.cookies[attr] >= 500)
        users = sorted(users, key=lambda user: getattr(user, attr), reverse=True)[:5]
        emojis = "🏆🥈🥉🏅🏅"
        tops = [f"{emoji} @{cookie.name} ({getattr(cookie, attr)})" for emoji, cookie in zip(emojis, users)]
        top = " ".join(tops)
        return await ctx.reply(f"top {len(users)} {title}: {top}")


def prepare(bot: Bobotinho) -> None:
    bot.add_cog(Cookie(bot))
