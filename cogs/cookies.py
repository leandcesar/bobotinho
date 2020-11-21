# -*- coding: utf-8 -*-

import random

from ext.command import command
from twitchio.ext import commands
from utils import convert


class Cookies(commands.AutoCog):
    def __init__(self, bot):
        self.bot = bot

    def _prepare(self, bot):
        pass

    @staticmethod
    def _get_cookie():
        with open("data//cookies.txt", "r", encoding="utf-8") as file:
            cookie = random.choice(file.readlines())
        return cookie

    async def _get_cooldown(self, ctx):
        timestamp = await self.bot.db.select1(
            "cookies", what="timestamp", where={"name": ctx.author.name}
        )
        return convert.cooldown(timestamp, 86400)

    async def _get_cookie_count(self, user: str):
        row = await self.bot.db.select(
            "cookies",
            what=["count", "you_gifted", "gifted_to_you", "gifts"],
            where={"name": user},
        )
        if not row:
            return "ainda não comeu nenhum cookie"
        gifts = f"(ainda tem {row[3]} cookies para comer)" if row[3] else ""
        return f"já comeu {row[0]} cookies, presenteou {row[1]} e foi presenteado com {row[2]} {gifts}"

    async def _set_gift(self, user: str):
        await self.bot.db.update(
            "cookies",
            values={"gifted_to_you": "gifted_to_you+1", "gifts": "gifts+1"},
            where={"name": user},
        )

    @command(description="receba a frase de um biscoito da sorte")
    async def cookie(self, ctx, x: str = None):
        if not await self.bot.db.exists("cookies", where={"name": ctx.author.name}):
            await self.bot.db.insert(
                "cookies",
                values={
                    "name": ctx.author.name,
                    "timestamp": ctx.message.timestamp,
                    "count": 1,
                },
            )
            ctx.response = f"@{ctx.author.name}: {self._get_cookie()} 🥠"
        elif x and x.isdigit():
            x = int(x)
            gifts = await self.bot.db.select1(
                "cookies", what="gifts", where={"name": ctx.author.name}
            )
            if x > gifts:
                ctx.response = f"@{ctx.author.name}, você não tem todos esses cookies para comer"
            else:
                await self.bot.db.update(
                    "cookies",
                    values={"count": f"count+{x}", "gifts": f"gifts-{x}"},
                    where={"name": ctx.author.name},
                )
                ctx.response = f"@{ctx.author.name}, você comeu {x} cookies de uma só vez 🥠"
        elif await self.bot.db.select1(
            "cookies", what="gifts", where={"name": ctx.author.name}
        ):
            await self.bot.db.update(
                "cookies",
                values={"count": "count+1", "gifts": "gifts-1"},
                where={"name": ctx.author.name},
            )
            if ctx.author.name == "kkalfoy":
                ctx.response = f"@{ctx.author.name}: orem para que não caiam em tentação. 🙏"
            else:
                ctx.response = f"@{ctx.author.name}: {self._get_cookie()} 🥠"
        else:
            cooldown = await self._get_cooldown(ctx)
            if cooldown:
                ctx.response = (
                    f"@{ctx.author.name}, aguarde {cooldown} para comer outro cookie ⌛"
                )
            else:
                await self.bot.db.update(
                    "cookies",
                    values={"count": "count+1", "timestamp": ctx.message.timestamp},
                    where={"name": ctx.author.name},
                )
                if ctx.author.name == "kkalfoy":
                    ctx.response = f"@{ctx.author.name}: orem para que não caiam em tentação. 🙏"
                else:
                    ctx.response = f"@{ctx.author.name}: {self._get_cookie()} 🥠"

    @command(aliases=["cc"], description="veja quantos cookies algum usuário já comeu")
    async def cookiecount(self, ctx, user: str = None):
        if not user:
            user = ctx.author.name

        user = convert.user(user)
        if user == self.bot.nick:
            ctx.response = f"@{ctx.author.name}, eu apenas faço os cookies"
        elif user == ctx.author.name:
            cookiecount = await self._get_cookie_count(ctx.author.name)
            ctx.response = f"@{ctx.author.name}, você {cookiecount}"
        else:
            cookiecount = await self._get_cookie_count(user)
            ctx.response = f"@{ctx.author.name}, @{user} {cookiecount}"

    @command(
        aliases=["give"],
        description="presenteie algum usuário com seu cookie",
        usage="digite o comando e o nome de alguém para presenteá-lo com seu cookie",
    )
    async def gift(self, ctx, user: str):
        user = convert.user(user)
        if user == self.bot.nick:
            ctx.response = f"@{ctx.author.name}, eu não quero seu cookie"
        elif user == ctx.author.name:
            ctx.response = f"@{ctx.author.name} tentou presentear ele mesmo..."
        else:
            if not await self.bot.db.exists("cookies", where={"name": ctx.author.name}):
                await self.bot.db.insert(
                    "cookies",
                    values={
                        "name": ctx.author.name,
                        "timestamp": ctx.message.timestamp,
                        "you_gifted": 1,
                    },
                )
                await self._set_gift(user)
                ctx.response = f"@{ctx.author.name} presenteou @{user} com um cookie 🎁"
            else:
                cooldown = await self._get_cooldown(ctx)
                if cooldown:
                    ctx.response = f"@{ctx.author.name}, aguarde {cooldown} para presentear um cookie ⌛"
                else:
                    await self.bot.db.update(
                        "cookies",
                        values={
                            "you_gifted": "you_gifted+1",
                            "timestamp": ctx.message.timestamp,
                        },
                        where={"name": ctx.author.name},
                    )
                    await self._set_gift(user)
                    ctx.response = (
                        f"@{ctx.author.name} presenteou @{user} com um cookie 🎁"
                    )

    @command(description="veja quais são os maiores comedores ou doadores de cookies", cooldown=15)
    async def top(self, ctx, orderby: str = "count"):
        if orderby.lower() in ("gift", "gifts", "give", "gives", "giver", "givers"):
            orderby = "you_gifted"
            title = "givers"
        else:
            orderby = "count"
            title = "cookiers"

        top = await self.bot.db.select_all(
            "cookies", what=["name", orderby], order_by=f"{orderby} desc", limit=5
        )
        emojis = ("🏆", "🥈", "🥉", "🏅", "🏅")
        tops = " ".join(
            [
                f'{emojis[i]} @{top[i]["name"]} ({str(top[i][orderby])})'
                for i in range(len(top))
            ]
        )
        ctx.response = f"@{ctx.author.name}, top {len(top)} {title}: {tops}"

    async def _slotmachine(self, ctx):
        a, b, c = random.choices("🍇🍊🍋🍒🍉🍐", k=3)
        if a == b == c:
            await self.bot.db.update(
                "cookies", values={"gifts": "gifts+7"}, where={"name": ctx.author.name},
            )
            return f"@{ctx.author.name} [{a}{b}{c}] você deu sorte, recuperou o cookie que apostou e ganhou mais 7 cookies! PogChamp"
        elif a == b or a == c or b == c:
            await self.bot.db.update(
                "cookies", values={"gifts": "gifts+2"}, where={"name": ctx.author.name},
            )
            return f"@{ctx.author.name} [{a}{b}{c}] você deu sorte, recuperou o cookie que apostou e ganhou mais 2 cookies!"
        else:
            await self.bot.db.update(
                "cookies",
                values={"timestamp": ctx.message.timestamp},
                where={"name": ctx.author.name},
            )
            return f"@{ctx.author.name} [{a}{b}{c}] você deu azar e perdeu o cookie que apostou..."

    @command(
        aliases=["slot", "sm"],
        description="aposte um cookie para ter a chance de ganhar outros... ou perdê-lo",
    )
    async def slotmachine(self, ctx):
        if not await self.bot.db.exists("cookies", where={"name": ctx.author.name}):
            await self.bot.db.insert("cookies", values={"name": ctx.author.name})
            ctx.response = await self._slotmachine(ctx)
        else:
            cooldown = await self._get_cooldown(ctx)
            if cooldown:
                ctx.response = (
                    f"@{ctx.author.name}, aguarde {cooldown} para apostar seu cookie ⌛"
                )
            else:
                ctx.response = await self._slotmachine(ctx)


def prepare(bot):
    bot.add_cog(Cookies(bot))


def breakdown(bot):
    pass
