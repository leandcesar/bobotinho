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

import random

from ext.command import command
from twitchio.ext import commands
from utils import convert


class Fun(commands.AutoCog):
    def __init__(self, bot):
        self.bot = bot
        self.fights = dict()

    def _prepare(self, bot):
        pass

    @command(
        aliases=["accept", "cancel", "deny"],
        description="desafie alguém do chat para lutar",
        cooldown=2,
        usage="digite o comando e o nome de alguém para desafiá-lo para luta",
    )
    async def fight(self, ctx, user: str = None):
        self.fights = {
            k: v
            for k, v in self.fights.items()
            if convert.cooldown(v["timestamp"], duration=120)
        }
        alias = ctx.command.invoked_by
        if alias == "accept":
            for k, v in self.fights.items():
                if ctx.author.name == v["user"]:
                    winner, loser = random.choice([(k, v["user"]), (v["user"], k)])
                    del self.fights[k]
                    quote = random.choice(
                        (
                            "@{winner} acaba com @{loser}",
                            "@{winner} deixa @{loser} desacordado",
                            "@{winner} derrota facilmente @{loser}",
                            "@{winner} espanca @{loser} sem piedade",
                            "@{winner} não dá chances para @{loser} e vence",
                            "@{winner} quase perde, mas derruba @{loser}",
                            "@{winner} vence a luta contra @{loser}",
                            "@{winner} vence com dificuldades @{loser}",
                            "@{winner} vence @{loser} em uma luta acirrada",
                            "@{winner} vence facilmente @{loser}",
                        )
                    )
                    ctx.response = (
                        f"{quote.format(winner=winner, loser=loser)}! PogChamp GG"
                    )
                    return
            ctx.response = f"@{ctx.author.name}, você não tem desafios para aceitar"
            return
        elif alias == "deny":
            for k, v in self.fights.items():
                if ctx.author.name == v["user"]:
                    del self.fights[k]
                    ctx.response = (
                        f"@{ctx.author.name} recusou o desafio contra @{k} LUL"
                    )
                    return
            ctx.response = f"@{ctx.author.name}, você não tem desafios para recusar"
            return
        elif alias == "cancel":
            if self.fights.pop(ctx.author.name, None):
                ctx.response = f"@{ctx.author.name} cancelou o desafio"
            else:
                ctx.response = (
                    f"@{ctx.author.name}, você não tem desafios para cancelar"
                )
            return
        if not user:
            return
        user = convert.user(user)
        if user == self.bot.nick:
            ctx.response = f"@{ctx.author.name}, você não conseguiria me derrotar..."
        elif user == ctx.author.name:
            ctx.response = f"@{ctx.author.name} iniciou uma luta interna contra ele mesmo... FeelsBadMan"
        elif ctx.author.name in self.fights.keys():
            ctx.response = (
                f"@{ctx.author.name}, você já desafiou alguém! "
                f'Digite "{ctx.prefix}cancel" para cancelar'
            )
        elif any([v for v in self.fights.values() if ctx.author.name == v["user"]]):
            ctx.response = (
                f"@{ctx.author.name}, você já está sendo desafiado por alguém! "
                f'Digite "{ctx.prefix}accept" ou "{ctx.prefix}deny"'
            )
        elif user in self.fights.keys():
            ctx.response = f"@{ctx.author.name}, @{user} já está desafiando alguém"
        elif any([v for v in self.fights.values() if user == v["user"]]):
            ctx.response = (
                f"@{ctx.author.name}, @{user} já está sendo desafiado por alguém"
            )
        else:
            self.fights[ctx.author.name] = dict(
                user=user, timestamp=ctx.message.timestamp
            )
            ctx.response = (
                f"@{user}, @{ctx.author.name} te desafiou! "
                f'Digite "{ctx.prefix}accept" ou "{ctx.prefix}deny" em até 2 minutos'
            )

    @command(
        description="dê um abraço em alguém do chat",
        cooldown=10,
        usage="digite o comando e o nome de alguém para abracá-lo",
    )
    async def hug(self, ctx, user: str):
        user = convert.user(user)
        if user == self.bot.nick:
            ctx.response = f"@{ctx.author.name}, 🤗"
        elif user == ctx.author.name:
            ctx.response = f"@{ctx.author.name} tentou abraçar ele mesmo..."
        else:
            ctx.response = f"@{ctx.author.name} abraçou @{user} 🤗"
            
    @command(
        name="4head",
        aliases=["hahaa"],
        description="receba uma piada, charada ou trocadilho",
        cooldown=20,
    )
    async def joke(self, ctx):
        with open("data//jokes.txt", "r", encoding="utf-8") as file:
            joke = random.choice(file.readlines())
        ctx.response = f"@{ctx.author.name}: {joke} 4Head"
            
    @command(
        aliases=["jankenpon", "jokempo"],
        description="tente vencer o pedra, papel e tesoura",
        usage="digite o comando e ✊, ✋ ou ✌",
    )
    async def jokenpo(self, ctx, choice):
        emoji = random.choice("✊✋✌")
        if choice == emoji:
            ctx.response = f"@{ctx.author.name}, {choice}x{emoji} e nós empatamos..."
        elif (choice, emoji) in [("✊","✋"), ("✋","✌"), ("✌","✊")]:
            ctx.response = f"@{ctx.author.name}, {choice}x{emoji} e eu consegui te prever facilmente"
        else:
            ctx.response = f"@{ctx.author.name}, {choice}x{emoji} e você deu sorte dessa vez"

    @command(
        description="dê um beijinho em alguém do chat",
        cooldown=10,
        usage="digite o comando e o nome de alguém para beijá-lo",
    )
    async def kiss(self, ctx, user: str):
        user = convert.user(user)
        if user == self.bot.nick:
            emoji = random.choice("😚😗😙😚😳😏")
            ctx.response = f"@{ctx.author.name}, {emoji} 💋"
        elif user == ctx.author.name:
            ctx.response = f"@{ctx.author.name} tentou beijar ele mesmo..."
        else:
            emoji = random.choice("😚😗😙😚😳😏")
            ctx.response = f"@{ctx.author.name} deu um beijinho em @{user} {emoji}💋"
        
    @command(
        aliases=["sadcat", "rsc"],
        description="receba a foto de um gatinho triste",
        cooldown=20,
    )
    async def randomsadcat(self, ctx):
        with open("data//sadcats.txt", "r", encoding="utf-8") as file:
            sadcat = "https://i.imgur.com/" + random.choice(file.readlines())
        ctx.response = f"@{ctx.author.name}, {sadcat} 😿"

    @command(
        description="coloque alguém do chat na cama para dormir",
        cooldown=10,
        usage="digite o comando e o nome de alguém para colocá-lo na cama",
    )
    async def tuck(self, ctx, user: str):
        user = convert.user(user)
        if user == self.bot.nick:
            ctx.response = f"@{ctx.author.name}, eu não posso dormir agora..."
        elif user == ctx.author.name:
            ctx.response = f"@{ctx.author.name} foi para a cama..."
        else:
            ctx.response = f"@{ctx.author.name} colocou @{user} na cama 🙂👉🛏"


def prepare(bot):
    bot.add_cog(Fun(bot))


def breakdown(bot):
    pass
