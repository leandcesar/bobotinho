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
import re

from ext.command import command
from twitchio.ext import commands


class Fun(commands.AutoCog):
    def __init__(self, bot):
        self.bot = bot

    def _prepare(self, bot):
        pass

    @command(
        name="%",
        aliases=["chance"],
        description="receba uma probabilidade de 0 a 100",
        cooldown=15,
    )
    async def chance(self, ctx):
        percentage = random.randint(0, 1000) / 10
        ctx.response = f"@{ctx.author.name}, {percentage}%"

    @command(
        aliases=["choose"],
        description='dê opções separadas por "ou" e uma delas será escolhida',
        usage='digite o comando e algumas opções separadas por "ou"',
    )
    async def choice(self, ctx, *, options: str):
        if not " ou " in options:
            return
        choice = random.choice(options.split(" ou ")).replace("?", "")
        ctx.response = f"@{ctx.author.name}, {choice}"

    @command(
        aliases=["coin", "cf"],
        description="jogue uma moeda e veja se deu cara ou coroa",
        cooldown=15,
    )
    async def coinflip(self, ctx):
        percentage = random.randint(0, 6000)  # Murray & Teare (1993)
        if percentage > 3000:
            ctx.response = f"@{ctx.author.name} jogou uma moeda e ela caiu em cara"
        elif percentage < 3000:
            ctx.response = f"@{ctx.author.name} jogou uma moeda e ela caiu em coroa"
        else:
            ctx.response = f"@{ctx.author.name} jogou uma moeda e ela caiu no meio, em pé! PogChamp"

    @command(
        aliases=["8ball", "magicball"],
        description="tenha sua pergunta respondida com uma previsão do 8-ball",
        cooldown=10,
        usage="digite o comando e uma pergunta para saber a resposta prevista",
    )
    async def eightball(self, ctx, *, question: str):
        quote = random.choice((
            "ao meu ver, sim",
            "com certeza",
            "com certeza não",
            "concentre-se e pergunte novamente",
            "decididamente sim",
            "definitivamente sim",
            "dificilmente",
            "é complicado...",
            "é melhor você não saber",
            "fontes dizem que não",
            "impossível isso acontecer",
            "impossível prever isso",
            "jamais",
            "muito duvidoso",
            "nunca",
            "não",
            "não conte com isso",
            "não é possível prever isso",
            "pergunta nebulosa, tente novamente",
            "pergunte novamente mais tarde...",
            "pode apostar que sim",
            "possivelmente",
            "provavelmente...",
            "sem dúvidas",
            "sim",
            "sinais apontam que sim",
            "talvez",
            "você ainda tem dúvidas?",
            "você não acreditaria...",
        ))
        ctx.response = f"@{ctx.author.name}, {quote} 🎱"

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
        aliases=["ship"],
        description="veja quanto de amor existe entre você e alguém ou algo",
        cooldown=10,
        usage="digite o comando e o nome de alguém ou algo para ver quanto há de amor",
    )
    async def love(self, ctx, *, something: str):
        emojis = ("😭", "😥", "💔", "😢", "😐", "😊", "❤", "💕", "💘", "😍", "PogChamp ❤")
        percentage = random.randint(0, 100)
        if re.match(r"([\w\s]+\s&\s[\w\s]+)+$", something):
            ctx.response = f"@{ctx.author.name}, entre {something}: {percentage}% de amor {emojis[round(percentage / 10)]}"
        else:
            ctx.response = f"@{ctx.author.name} & {something}: {percentage}% de amor {emojis[round(percentage / 10)]}"

    @command(
        description="sorteie uma palavra da mensagem informada",
        usage="digite o comando e uma mensagem para sortear uma das palavras nela",
    )
    async def pick(self, ctx, *, message: str):
        picked = random.choice(message.split())
        ctx.response = f"@{ctx.author.name}, {picked}"

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
        description="role um dado e veja o resultado",
        cooldown=15,
        usage="digite o comando e o(s) dado(s) que quer rolar no formato <quantidade>d<lados> (ex: 1d20)",
    )
    async def roll(self, ctx, dices: str):
        dices = dices.lower().split("d")
        amount = float(dices[0].replace(",", "."))
        sides = float(dices[1].replace(",", "."))
        if not dices[0]:
            ctx.response = f"@{ctx.author.name}, especifique a quantidade de dados"
        elif not dices[1]:
            ctx.response = (
                f"@{ctx.author.name}, especifique a quantidade de lados do dado"
            )
        elif amount > 1e6:
            ctx.response = f"@{ctx.author.name}, eu não tenho tantos dados"
        elif amount == 0:
            ctx.response = f"@{ctx.author.name}, eu não consigo rolar sem dados"
        elif amount < 0:
            ctx.response = f"@{ctx.author.name}, não tente tirar meus dados de mim"
        elif amount % 1 != 0:
            ctx.response = f"@{ctx.author.name}, eu não posso dividir meus dados"
        elif sides > 1e6:
            ctx.response = (
                f"@{ctx.author.name}, eu não tenho dados com tantos lados"
            )
        elif sides == 1:
            ctx.response = (
                f"@{ctx.author.name}, um dado de {dices[1]} lado? "
                f"Esse é um exercício topológico interessante..."
            )
        elif sides <= 0 or sides % 1 != 0:
            ctx.response = (
                f"@{ctx.author.name}, um dado de {dices[1]} lados? "
                f"Esse é um exercício topológico interessante..."
            )
        else:
            roll = sum(
                [random.randint(1, round(sides)) for i in range(round(amount))]
            )
            ctx.response = f"@{ctx.author.name} rolou {roll} 🎲"


def prepare(bot):
    bot.add_cog(Fun(bot))


def breakdown(bot):
    pass
