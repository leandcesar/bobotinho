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
import json
import random

from ext.command import command
from twitchio.ext import commands
from unidecode import unidecode
from utils import convert


class Dungeons(commands.AutoCog):
    def __init__(self, bot):
        self.bot = bot
        with open("data//dungeons.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            self.dungeons = data["eds"]
            self.classes = data["classes"]

    def _prepare(self, bot):
        pass

    async def _choose_class(self, ctx, choice: str = ""):
        choice = unidecode(choice).lower()
        for k, v in self.classes.items():
            if choice == v.get("0").lower():
                class_ = int(k)
                subclass = v.get("0")
                await self.bot.db.insert(
                    "dungeons",
                    values={
                        "name": ctx.author.name,
                        "channel": ctx.channel.name,
                        "class_": class_,
                        "subclass": subclass,
                    },
                )
                return f'@{ctx.author.name}, você escolheu {subclass}! {["⚔️", "🏹", "🧙"][class_ // 4]}'
        return (
            f"@{ctx.author.name}, antes de continuar, escolha sua classe! "
            f'Digite "%ed" e: guerreiro(a), arqueiro(a) ou mago(a)'
        )

    async def _choose_subclass(self, ctx, choice: str = ""):
        choice = unidecode(choice).lower()
        class_ = await self.bot.db.select1(
            "dungeons", what="class_", where={"name": ctx.author.name}
        )
        class_ = abs(class_)
        if choice == unidecode(self.classes.get(str(class_))["3"]).lower():
            subclass = self.classes.get(str(class_))["3"]
        elif choice == unidecode(self.classes.get(str(class_ + 1))["3"]).lower():
            class_ += 1
            subclass = self.classes.get(str(class_ + 1))["3"]
        else:
            op1 = self.classes[str(class_)]["3"]
            op2 = self.classes[str(class_ + 1)]["3"]
            return f'@{ctx.author.name}, antes de continuar, digite "%ed" e sua nova classe: {op1} ou {op2}'
        await self.bot.db.update(
            "dungeons",
            values={"class_": class_, "subclass": subclass},
            where={"name": ctx.author.name},
        )
        return f"@{ctx.author.name}, agora você é {subclass}!"

    async def _result_dungeon(self, ctx, dungeon_id: str, choice: str):
        result = random.choices(["win", "lose"], weights=(0.66, 0.33), k=1)[0]
        dungeon = self.dungeons[dungeon_id][choice][result]
        if result == "win":
            row = await self.bot.db.select(
                "dungeons",
                what=["level", "xp", "class_", "subclass"],
                where={"name": ctx.author.name},
            )

            level = row["level"]
            gained = random.randint(50, 75) + 3 * row["level"]
            xp = row["xp"] + gained
            class_ = row["class_"]
            subclass = row["subclass"]
            dungeon += f" +{gained} XP"

            if xp > 100 * (row["level"]) + 25 * sum(range(1, row["level"] + 1)):
                level = row["level"] + 1
                if level % 10 == 0 and level < 70:
                    dungeon += f", alcançou level {level} ⬆"
                    if level // 10 == 3:
                        op1 = self.classes[str(class_)]["3"]
                        op2 = self.classes[str(class_ + 1)]["3"]
                        class_ = -row["class_"]
                        subclass = None
                        dungeon += (
                            f' e pode se tornar "%ed {op1}" ou "%ed {op2}"! PogChamp'
                        )
                    else:
                        subclass = self.classes[str(class_)][
                            str(level // 10 if level // 10 < 7 else 6)
                        ]
                        dungeon += f" e se tornou {subclass} PogChamp"
                else:
                    dungeon += f" e alcançou level {level} ⬆"
            await self.bot.db.update(
                "dungeons",
                values={
                    "wins": "wins+1",
                    "class_": class_,
                    "subclass": subclass,
                    "level": level,
                    "xp": xp,
                    "ed": None,
                    "channel": ctx.channel.name,
                    "timestamp": ctx.message.timestamp,
                },
                where={"name": ctx.author.name},
            )
        else:
            await self.bot.db.update(
                "dungeons",
                values={
                    "losses": "losses+1",
                    "ed": None,
                    "channel": ctx.channel.name,
                    "timestamp": ctx.message.timestamp,
                },
                where={"name": ctx.author.name},
            )
            dungeon += " 0 XP"
        return dungeon

    async def _get_dungeon(self, ctx, dungeon_id=None):
        if not dungeon_id:
            dungeon_id = random.randint(1, len(self.dungeons))
            await self.bot.db.update(
                "dungeons", values={"ed": str(dungeon_id)}, where={"name": ctx.author.name}
            )

        return self.dungeons[str(dungeon_id)]["dungeon"]

    async def _get_level(self, user: str):
        row = await self.bot.db.select("dungeons", where={"name": user})
        if not row:
            return "ainda não entrou em nenhuma dungeon"

        subclass = row["subclass"]
        level = row["level"]
        xp = row["xp"]
        wins = row["wins"]
        losses = row["losses"]
        winrate = (wins / (wins + losses)) * 100 if wins or losses else 0
        return (
            f"é {subclass} ({level}, {xp} XP) com {wins + losses} dungeons "
            f"({wins} vitórias, {losses} derrotas, {winrate:.2f}% winrate) ♦"
        )

    async def _get_rank(self, what=["name", "level", "xp"], where={}, order_by="level desc, xp desc"):
        return await self.bot.db.select_all(
            "dungeons", what=what, where=where, order_by=order_by, limit=5
        )

    @command(
        aliases=["ed", "ed1", "ed2"],
        description="entre na dungeon, faça sua escolha e adquira experiência",
        cooldown=1,
    )
    async def enterdungeon(self, ctx, *, choice: str = ""):
        if not await self.bot.db.exists("dungeons", where={"name": ctx.author.name}):
            ctx.response = await self._choose_class(ctx, choice)
        elif (
            await self.bot.db.select1("dungeons", what="class_", where={"name": ctx.author.name}) < 0
        ):
            ctx.response = await self._choose_subclass(ctx, choice)
        else:
            timestamp = await self.bot.db.select1(
                "dungeons", what="timestamp", where={"name": ctx.author.name}
            )
            cooldown = convert.cooldown(timestamp, 10800)
            if cooldown:
                ctx.response = f"@{ctx.author.name}, aguarde {cooldown} para entrar em outra dungeon ⌛"
            else:
                if ctx.command.invoked_by in ("ed1", "ed2"):
                    choice = ctx.command.invoked_by[-1]
                dungeon_id = await self.bot.db.select1(
                    "dungeons", what="ed", where={"name": ctx.author.name}
                )
                if not dungeon_id:
                    dungeon = await self._get_dungeon(ctx)
                elif choice in ("1", "2"):
                    dungeon = await self._result_dungeon(ctx, str(dungeon_id), choice)
                else:
                    dungeon = await self._get_dungeon(ctx, str(dungeon_id))
                ctx.response = f"@{ctx.author.name}: {dungeon}"

    @command(
        aliases=["fed"],
        description="entre na dungeon e adquira experiência sem precisar tomar uma escolha",
        cooldown=1,
    )
    async def fasted(self, ctx):
        if not await self.bot.db.exists("dungeons", where={"name": ctx.author.name}):
            ctx.response = await self._choose_class(ctx)
        elif (
            await self.bot.db.select1("dungeons", what="class_", where={"name": ctx.author.name}) < 0
        ):
            ctx.response = await self._choose_subclass(ctx)
        else:
            timestamp = await self.bot.db.select1(
                "dungeons", what="timestamp", where={"name": ctx.author.name}
            )
            cooldown = convert.cooldown(timestamp, 10800)
            if cooldown:
                ctx.response = f"@{ctx.author.name}, aguarde {cooldown} para entrar em outra dungeon ⌛"
            else:
                dungeon_id = str(random.randint(1, len(self.dungeons)))
                choice = random.randint(1, 2)
                dungeon, eds = self.dungeons[dungeon_id]["dungeon"].split('"%ed 1"')
                dungeon += (
                    eds.split('ou "%ed 2"')[choice - 1]
                    .replace("para", "Você decide", 1)
                    .rstrip()
                    + ". "
                )
                dungeon += await self._result_dungeon(ctx, dungeon_id, str(choice))
                ctx.response = f"@{ctx.author.name}: {dungeon}"

    @command(
        aliases=["lvl"],
        description="veja qual o seu level (ou de alguém) e outras estatísticas da dungeon",
    )
    async def level(self, ctx, user: str = None):
        if not user:
            user = ctx.author.name

        user = convert.user(user)
        if user == self.bot.nick:
            ctx.response = f"@{ctx.author.name}, eu apenas crio as dungeons..."
        elif user == ctx.author.name:
            level = await self._get_level(ctx.author.name)
            ctx.response = f"@{ctx.author.name}, você {level}"
        else:
            level = await self._get_level(user)
            ctx.response = f"@{ctx.author.name}, @{user} {level}"

    @command(description="saiba quais são os melhores jogadores da dungeon")
    async def rank(self, ctx, orderby: str = "dungeons"):
        orderby = orderby.lower()
        if orderby in ("guerreiro", "guerreiros"):
            rank = await self._get_rank(
                where={("class_", ">="): 1, ("class_", "<="): 4}
            )
        elif orderby in ("arqueiro", "arqueiros"):
            rank = await self._get_rank(
                where={("class_", ">="): 5, ("class_", "<="): 8}
            )
        elif orderby in ("mago", "magos"):
            rank = await self._get_rank(
                where={("class_", ">="): 9, ("class_", "<="): 12}
            )
        elif orderby in ("vitoria", "vitorias", "vitória", "vitórias", "win", "wins"):
            rank = await self._get_rank(what=["name", "wins"], order_by="wins desc")
            orderby = "vitórias"
        elif orderby in ("derrota", "derrotas", "lose", "losses"):
            rank = await self._get_rank(what=["name", "losses"], order_by="losses desc")
            orderby = "derrotas"
        elif orderby == "winrate":
            rank = await self._get_rank(
                what=["name", "wins/(wins+losses) as winrate"],
                order_by="1.0 * wins / losses desc",
            )
        elif orderby == "loserate":
            rank = await self._get_rank(
                what=["name", "losses/(wins+losses) as loserate"],
                order_by="1.0 * wins / losses asc",
            )
        else:
            rank = await self._get_rank()
            orderby = "dungeons"

        emojis = ("🏆", "🥈", "🥉", "🏅", "🏅")
        
        tops = " ".join(
            [
                "{0} @{1} ({2})".format(
                    emojis[i], 
                    rank[i]["name"], 
                    rank[i]["wins"]
                    if orderby == "vitórias"
                    else rank[i]["losses"]
                    if orderby == "derrotas"
                    else round(rank[i]["winrate"] * 100, 1)
                    if orderby == "winrate"
                    else round(rank[i]["loserate"] * 100, 1)
                    if orderby == "loserate"
                    else f'{rank[i]["level"]}, {rank[i]["xp"]} XP'
                )
                for i in range(len(rank))
            ]
        )
        ctx.response = f"@{ctx.author.name}, top {len(rank)} {orderby}: {tops}"


def prepare(bot):
    bot.add_cog(Dungeons(bot))


def breakdown(bot):
    pass
