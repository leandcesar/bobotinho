# -*- coding: utf-8 -*-

"""
bobotinho - Twitch bot for Brazilian offstream chat entertainment
Copyright (C) 2020  Leandro César

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import asyncio
import random
import datetime

from ext.command import command
from twitchio.ext import commands
from utils import convert


class Cookies(commands.AutoCog):
    def __init__(self, bot):
        self.bot = bot
        self.marriages = dict()
        self.pets = {              
            "peixe": [10, 2, "🐟"],
            "pássaro": [20, 4, "🐦"],
            "hamster": [30, 6, "🐹"], 
            "coelho": [40, 8, "🐰"],
            "cachorro": [50, 10, "🐶"], 
            "gato": [50, 10, "🐱"],
            "cobra": [70, 14, "🐍"],
            "lobo": [85, 17, "🐺"], 
            "panda": [100, 20, "🐼"],
            "leão": [150, 30, "🦁"], 
            "unicórnio": [200, 50, "🦄"], 
            "dragão": [999, 100, "🐲"],
        }

    def _prepare(self, bot):
        pass

    @staticmethod
    def _get_cookie():
        with open("data//cookies.txt", "r", encoding="utf-8") as file:
            cookie = random.choice(file.readlines())
        return cookie

    async def _get_cookie_count(self, user: str):
        row = await self.bot.db.select(
            "cookies",
            what=["count", "you_gifted", "gifted_to_you", "gifts"],
            where={"name": user},
        )
        if not row:
            return "ainda não comeu nenhum cookie"
        gifts = f"(tem {row[3]} cookies estocados)" if row[3] else ""
        return f"já comeu {row[0]} cookies, presenteou {row[1]} e foi presenteado com {row[2]} {gifts}"

    async def _set_gift(self, user: str):
        await self.bot.db.update(
            "cookies",
            values={"gifted_to_you": "gifted_to_you+1", "gifts": "gifts+1"},
            where={"name": user},
        )

    @command(description="coma um biscoito da sorte e receba uma frase")
    async def cookie(self, ctx, amount: str = None):
        if not await self.bot.db.exists("cookies", where={"name": ctx.author.name}):
            await self.bot.db.insert(
                "cookies",
                values={
                    "name": ctx.author.name,
                    "count": 1,
                    "daily": False,
                },
            )
            ctx.response = f"@{ctx.author.name}: {self._get_cookie()} 🥠"
        elif amount and amount.isdigit() and int(amount) > 0:
            amount = int(amount)
            gifts = await self.bot.db.select1(
                "cookies", what="gifts", where={"name": ctx.author.name}
            )
            if amount > gifts:
                ctx.response = f"@{ctx.author.name}, você não tem todos esses cookies para comer"
            else:
                await self.bot.db.update(
                    "cookies",
                    values={"count": f"count+{amount}", "gifts": f"gifts-{amount}"},
                    where={"name": ctx.author.name},
                )
                ctx.response = f"@{ctx.author.name}, você comeu {amount} cookies de uma só vez 🥠"
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
        elif await self.bot.db.select1("cookies", what="daily", where={"name": ctx.author.name}):
            await self.bot.db.update(
                "cookies",
                values={"count": "count+1", "daily": False},
                where={"name": ctx.author.name},
            )
            if ctx.author.name == "kkalfoy":
                ctx.response = f"@{ctx.author.name}: orem para que não caiam em tentação. 🙏"
            else:
                ctx.response = f"@{ctx.author.name}: {self._get_cookie()} 🥠"
        else:
            ctx.response = (
                f"@{ctx.author.name}, você já usou seu cookie diário, a próxima fornada sai às 6 da manhã! ⌛"
            )
                
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

    @command(description="divorcie-se da pessoa com quem você é casada")
    async def divorce(self, ctx, user: str = None):
        if not await self.bot.db.select1("users", what="married", where={"name": ctx.author.name}):
            ctx.response = (
                f"@{ctx.author.name}, você só pode usar esse comando se estiver casado"
            )
        elif not user:
            ctx.response = (
                f"@{ctx.author.name}, parece que o casamento não deu nada certo... "
                f'caso tenha certeza, digite "{ctx.prefix}divorce" e o nome da pessoa com quem se casou'
            )
        else:
            user = convert.user(user)
            married = await self.bot.db.select1(
                "users", what="married", where={"name": user}
            )
            if int(married) == ctx.author.id:
                ctx.response = (
                    f"@{ctx.author.name}, então, é isso... da próxima vez, " 
                    "case-se com alguém que realmente te ame, e não qualquer pessoa por aí"
                )
                await self.bot.db.update(
                    "users", 
                    values={
                        "divorces": "divorces+1", 
                        "married": None, 
                        "marriage": None
                    }, 
                    where={"name": user},
                )
                await self.bot.db.update(
                    "users", 
                    values={
                        "divorces": "divorces+1", 
                        "married": None, 
                        "marriage": None
                    }, 
                    where={"name": ctx.author.name},
                )
            else:
                ctx.response = (
                    f"@{ctx.author.name}, você não sabe nem o nome da pessoa com quem está casado?"
                )

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
        elif not await self.bot.db.exists("cookies", where={"name": ctx.author.name}):
            await self.bot.db.insert(
                "cookies",
                values={
                    "name": ctx.author.name,
                    "daily": False,
                    "you_gifted": 1,
                },
            )
            await self._set_gift(user)
            ctx.response = f"@{ctx.author.name} presenteou @{user} com um cookie 🎁"
        elif await self.bot.db.select1("cookies", what="daily", where={"name": ctx.author.name}):
            await self.bot.db.update(
                "cookies",
                values={
                    "you_gifted": "you_gifted+1",
                    "daily": False,
                },
                where={"name": ctx.author.name},
            )
            await self._set_gift(user)
            ctx.response = (
                f"@{ctx.author.name} presenteou @{user} com um cookie 🎁"
            )
        else:
            ctx.response = f"@{ctx.author.name}, você já usou seu cookie diário, a próxima fornada sai às 6 da manhã! ⌛"

    @command(
        aliases=["ma"],
        description="saiba há quanto tempo algum usuário está casado", 
    )
    async def marriage(self, ctx, user: str = None):
        if not user:
            user = ctx.author.name
        elif user == self.bot.nick:
            ctx.response = f"@{ctx.author.name}, nunca me casarei com ninguém"
            return
        else:
            user = convert.user(user)
            if not await self.bot.db.exists("users", what="name", where={"name": user}):
                ctx.response = (
                    f"@{ctx.author.name}, @{user} ainda não foi registrado "
                    f"(o usuário precisa ter usado algum comando)"
                )
                return
        marry = await self.bot.db.select(
            "users", what=["married", "marriage"], where={"name": user}
        )
        user = "você" if user == ctx.author.name else f"@{user}"
        if not marry["married"]:
            ctx.response = (
                f"@{ctx.author.name}, {user} não se casou com ninguém"
            )
        else:
            married = await self.bot.db.select1(
                "users", what="name", where={"id": marry["married"]}
            )
            married = "você" if married == ctx.author.name else f"@{married}"
            marriage = convert.timesince(marry["marriage"])
            ctx.response = (
                f"@{ctx.author.name}, {user} se casou com {married} há {marriage}"
            )
    
    @command(
        aliases=["yes", "no"],
        description="case-se e seja feliz para sempre, mas isso custará cookies, então escolha a pessoa certa", 
        usage="digite o comando e o nome de quem você quer pedir em casamento, mas saiba: uma aliança custa caro")
    async def marry(self, ctx, user: str = None):
        self.marriages = {
            k: v
            for k, v in self.marriages.items()
            if convert.cooldown(v["timestamp"], duration=180)
        }
        alias = ctx.command.invoked_by
        if alias == "yes":
            for k, v in self.marriages.items():
                if ctx.author.name == v["user"]:
                    if await self.bot.db.select1("cookies", what="gifts", where={"name": k}) < 100:
                        ctx.response = (
                            f"@{ctx.author.name}, aparentemente @{k} gastou todos os cookies que eram pra aliança "
                            "e por isso o casamento precisou ser cancelado"
                        )
                    else:
                        await self.bot.db.update(
                            "users", values={"married": ctx.author.id, "marriage": ctx.message.timestamp}, where={"name": k},
                        )
                        await self.bot.db.update(
                            "users", values={"married": v["id"], "marriage": ctx.message.timestamp}, where={"name": ctx.author.name},
                        )
                        ctx.response = (
                            f"@{ctx.author.name} aceitou se casar com @{k}, felicidades para os dois! 🎉💞"
                        )
                        await self.bot.db.update(
                            "cookies", values={"gifts": "gifts-100"}, where={"name": k},
                        )
                        del self.marriages[k]
                    return
            ctx.response = f"@{ctx.author.name}, não há nenhum pedido de casamento para você"
            return
        elif alias == "no":
            for k, v in self.marriages.items():
                if ctx.author.name == v["user"]:
                    ctx.response = (
                        f"@{ctx.author.name} recusou o pedido de casamento de @{k}... 💔"
                    )
                    del self.marriages[k]
                    return
            ctx.response = f"@{ctx.author.name}, não há nenhum pedido de casamento para você"
            return
        if not user:
            return
        user = convert.user(user)
        if user == "kkalfoy":
            ctx.response = f"@{ctx.author.name}, sai."
        elif user == self.bot.nick:
            ctx.response = f"@{ctx.author.name}, não fui programado para fazer parte de um relacionamento"
        elif user == ctx.author.name:
            ctx.response = f"@{ctx.author.name} tentou se casar com ele mesmo... FeelsBadMan"
        elif ctx.author.name in self.marriages.keys():
            ctx.response = (
                f"@{ctx.author.name}, vá com calma garanhão, você acabou de pedir alguém em casamento!"
            )
        elif any([v for v in self.marriages.values() if ctx.author.name == v["user"]]):
            ctx.response = (
                f"@{ctx.author.name}, antes, você precisa responder ao pedido que lhe fizeram! "
                f'Digite "{ctx.prefix}yes" ou "{ctx.prefix}no"'
            )
        elif user in self.marriages.keys():
            ctx.response = f"@{ctx.author.name}, @{user} está aguardando a resposta de outra pessoa"
        elif any([v for v in self.marriages.values() if user == v["user"]]):
            ctx.response = (
                f"@{ctx.author.name}, alguém chegou primeiro e já pediu a mão de @{user}"
            )
        elif await self.bot.db.select1("users", what="married", where={"name": ctx.author.name}):
            ctx.response = (
                f"@{ctx.author.name}, traição é inaceitável, ao menos se divorcie (%divorce) antes de partir pra outra"
            )
        elif not await self.bot.db.exists("users", where={"name": user}):
            ctx.response = (
                f"@{ctx.author.name}, @{user} ainda não foi registrado "
                f"(o usuário precisa ter usado algum comando)"
            )
        elif await self.bot.db.select1("users", what="married", where={"name": user}):
            ctx.response = (
                f"@{ctx.author.name}, controle seu desejo por pessoas casadas, @{user} já está em um compromisso"
            )
        elif await self.bot.db.select1("cookies", what="gifts", where={"name": ctx.author.name}) < 100:
            ctx.response = (
                f"@{ctx.author.name}, o casamento é algo importante e seu amor merece o melhor, "
                f"por isso para comprar uma ótima aliança você deve ter 100 cookies estocados"
            )
        else:
            self.marriages[ctx.author.name] = dict(
                user=user, timestamp=ctx.message.timestamp, id=ctx.author.id,
            )
            ctx.response = (
                f"@{user}, você aceita se casar com @{ctx.author.name}? 💐💍"
                f'Digite "{ctx.prefix}yes" ou "{ctx.prefix}no"'
            )

    @command(
        description="troque seus cookies por um pet e tenha um novo companheiro",
        cooldown=2,
    )
    async def pet(self, ctx, action: str = None, option: str = None):
        if action:
            action = action.lower()
        if option:
            option = option.lower()
        if action == "list":
            pets = ", ".join([f"{k} ({v[0]})" for k, v in self.pets.items()])
            ctx.response = f'@{ctx.author.name}, adquira com "%pet buy" e: {pets}'
        elif action == "buy" and not option in self.pets.keys():
            ctx.response = f"@{ctx.author.name}, escolha um pet que esteja disponível na lista (%pet list)"
        elif action == "buy":
            pet = self.pets[option]
            price = pet[0]
            emoji = pet[2]
            if await self.bot.db.select1("cookies", what="gifts", where={"name": ctx.author.name}) < price:
                ctx.response = f"@{ctx.author.name}, você precisa de {price} cookies estocados para adquirir um {option} {emoji}"
            else:
                await self.bot.db.update(
                    "cookies", values={"gifts": f"gifts-{price}"}, where={"name": ctx.author.name},
                )
                await self.bot.db.update(
                    "users", values={"pet": option, "petname": None}, where={"name": ctx.author.name},
                )
                ctx.response = (
                    f"@{ctx.author.name}, você adquiriu um {option} {emoji}! "
                    "Escolha um nome com %pet name e o nome que desejar"
                )
        elif action == "name" and not option:
            ctx.response = f"@{ctx.author.name}, escolha um nome com %pet name e o nome que desejar"
        elif action == "name" and len(option) > 20:
            ctx.response = f"@{ctx.author.name}, esse nome é muito comprido para seu pet"
        elif action == "name":
            await self.bot.db.update(
                "users", values={"petname": option.title()}, where={"name": ctx.author.name},
            )
            ctx.response = f"@{ctx.author.name}, agora seu pet se chama {option.title()}"
        else:
            if not action:
                action = ctx.author.name
            user = convert.user(action)
            pet = await self.bot.db.select("users", what=["pet", "petname"], where={"name": user})
            user = "você" if user == ctx.author.name else f"@{user}"
            if pet["pet"]:
                emoji = self.pets[pet["pet"]][2]
                if pet["petname"]:
                    ctx.response = f'@{ctx.author.name}, {user} possui um {pet["pet"]} chamado {pet["petname"]} {emoji}'
                else:
                    ctx.response = f'@{ctx.author.name}, {user} possui um {pet["pet"]} {emoji}'
            elif user == "você":
                ctx.response = f"@{ctx.author.name}, adquira um pet em troca de cookies (%pet list)"
            else:
                ctx.response = f"@{ctx.author.name}, {user} não possui um pet"

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
                values={"daily": False},
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
        elif not await self.bot.db.select1("cookies", what="daily", where={"name": ctx.author.name}):
            ctx.response = (
                f"@{ctx.author.name}, você já usou seu cookie diário, a próxima fornada sai às 6 da manhã! ⌛"
            )
        else:
            ctx.response = await self._slotmachine(ctx)

    @command(
        description="estoque o seu cookie diário caso não queira comê-lo",
    )
    async def stock(self, ctx):
        if not await self.bot.db.exists("cookies", where={"name": ctx.author.name}):
            await self.bot.db.insert("cookies", values={"name": ctx.author.name})
        if not await self.bot.db.select1("cookies", what="daily", where={"name": ctx.author.name}):
            ctx.response = (
                f"@{ctx.author.name}, você já usou seu cookie diário, a próxima fornada sai às 6 da manhã! ⌛"
            )
        else:
            await self.bot.db.update(
                "cookies",
                values={"daily": False, "gifts": "gifts+1"},
                where={"name": ctx.author.name},
            )
            ctx.response = f"@{ctx.author.name}, você estocou seu cookie diário"


async def reset_daily(bot):
    while True:
        current = datetime.datetime.utcnow().time() 
        target = datetime.time(9, 0, 0)
        if current.hour < 9:
            hour = target.hour - current.hour - 1
        else:
            hour = 24 - (current.hour - target.hour) - 1
        minute = 60 - current.minute - 1
        second = 60 - current.second
        delta = second + minute * 60 + hour * 3600
        await asyncio.sleep(delta, loop=bot.loop)
        await bot.db.update("cookies", values={"daily": True}, where={"daily": False})


def prepare(bot):
    bot.add_cog(Cookies(bot))
    bot.loop.create_task(reset_daily(bot))


def breakdown(bot):
    pass
