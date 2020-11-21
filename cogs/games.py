# -*- coding: utf-8 -*-

import asyncio
import inspect
import random
import re

from ext.command import command
from twitchio.ext import commands
from unidecode import unidecode
from utils import asyncrq, dicio, checks


class Games(commands.AutoCog):
    def __init__(self, bot):
        self.bot = bot
        self.running = dict()
        self.dicio = dicio.Dicio()

    def _prepare(self, bot):
        pass

    @staticmethod
    def _get_pattern():
        return random.choice(
            (
                "ba", "be", "bi", "bra", "bri",
                "ca", "ção", "ce", "cha", "co", 
                "com", "cos", "cra", "cre", "cri", 
                "da", "de", "den", "do", "dra", 
                "em", "es", 
                "fa", "fo", "fra", "fri", 
                "ga", "gui", "gue", 
                "ja", "je",
                "la", "le", "lar", "lha", "lho", 
                "ma", "me", "mi", "men", 
                "na", "ne", "no", "nha", "nho", 
                "pa", "pe", "po", "pra", "pri", "pro", 
                "ra", "re", "ri", "ro", 
                "sa", "se", "so", 
                "ta", "te", "to", "tra", "tri", 
                "va", "ve", "vo",
            )
        )

    @staticmethod
    def _get_word():
        with open("data//words.txt", "r", encoding="utf-8") as file:
            word = random.choice(file.readlines())
        return word

    async def _checks_wordplay(self, run, message):
        word = message.content.lower().strip()
        return (
            word.isalpha()
            and word.find(run["pattern"]) != -1 
            and not word in run["already"]
            and await self.dicio.exists(word) 
        )

    def _checks_hangman(self, run, message):
        letter = message.content.lower().strip()
        return (
            len(letter) == 1 
            and letter.isalpha() 
            and not unidecode(letter) in list(run["corrects"]) + list(run["wrongs"])
        )

    def _update_wordplay_longest(self, message):
        word = message.content.lower().strip()
        run = self.running[message.channel.name]
        if len(word) > len(run["longest"][1]):
            run["longest"] = (message.author.name, word)
        self.running[message.channel.name] = run

    def _update_wordplay_most(self, message):
        author = message.author.name
        run = self.running[message.channel.name]
        run["already"].append(message.content.lower().strip())
        if run["players"].get(author, False):
            run["players"][author] += 1
        else:
            run["players"][author] = 1
        if run["players"][author] > run["most"][1]:
            run["most"] = (author, run["players"][author])
        self.running[message.channel.name] = run

    async def _update_hangman(self, message):
        run = self.running[message.channel.name]
        letter = unidecode(message.content.lower().strip())
        word = run["word"]
        if letter in unidecode(word):
            run["corrects"][letter] = message.author.name
        else:
            run["wrongs"][letter] = message.author.name
        self.running[message.channel.name] = run
        word_ = ""
        for char in word:
            if unidecode(char) in run["corrects"] or char == "-":
                word_ += char
            else:
                word_ += "_"
        if word_ == word:
            corrects = dict()
            for v in run["corrects"].values():
                if v in corrects:
                    corrects[v] += 1
                else:
                    corrects[v] = 1
            corrects = sorted(corrects.items(), key=lambda x: x[1], reverse=True)
            corrects = "@" + ", @".join([f"{x[0]} ({x[1]})" for x in corrects])
            await message.channel.send(
                f'fim de jogo, os usuários descobriram a palavra "{word_}": 🏆 {corrects}'
            )
            del self.running[message.channel.name]
        elif letter in unidecode(word):
            await message.channel.send(
                f'@{message.author.name} acertou com a letra "{letter.upper()}": {word_}'
            )
        elif len(run["wrongs"]) == 5:
            await message.channel.send(
                f'fim de jogo, @{message.author.name} errou a última tentativa com a letra "{letter.upper()}"... 👎'
            )
            del self.running[message.channel.name]
        else:
            await message.channel.send(
                f'@{message.author.name} errou com a letra "{letter.upper()}" '
                f'e agora resta(m) {5 - len(run["wrongs"])} tentativa(s): {word_}'
            )

    async def answers(self, message):
        run = self.running.get(message.channel.name, False)
        if run:
            checks = run["checks"]
            if inspect.iscoroutinefunction(checks):
                check = await checks(run, message)
            else:
                check = checks(run, message)
            if check:
                update = run["update"]
                if inspect.iscoroutinefunction(update):
                    await update(message)
                else:
                    update(message)
    
    @command(
        aliases=["lw"],
        description='jogo de palavras: quem enviar a palavra mais comprida com determida sílaba vence', 
        cooldown=5,
        level="admin",
    )
    @commands.check(checks.is_admin)
    async def longestword(self, ctx):
        if not self.running.get(ctx.channel.name, False):
            pattern = self._get_pattern()
            self.running[ctx.channel.name] = {
                "checks": self._checks_wordplay,
                "update": self._update_wordplay_longest,
                "pattern": pattern,
                "already": [],  # ["word1", "word2", ...]
                "longest": [None, ""],  # ["user", "longest_word"]
                "most": [None, 0],  # ["user", count]
                "players": {},  # {"user1": count, "user2": count, ...}
            }
            await ctx.send(
                f"@{ctx.author.name} iniciou um novo jogo: "
                f'envie a maior palavra que contiver a sílaba "{pattern.upper()}"! '
                "Acaba em 30 segundos, valendo!"
            )
            try:
                await asyncio.wait_for(
                    asyncio.sleep(60, loop=self.bot.loop), 
                    timeout=30, 
                    loop=self.bot.loop, 
                )
            except asyncio.TimeoutError:
                winner = self.running[ctx.channel.name]["longest"]
                del self.running[ctx.channel.name]
                if winner[0]:
                    ctx.response = f'fim de jogo! @{winner[0]} venceu com a palavra "{winner[1]}" 🏆'
                else:
                    ctx.response = "fim de jogo, ninguém respondeu corretamente... 👎"
            except Exception as err:
                raise err
        else:
            ctx.response = f"@{ctx.author.name}, um jogo já está em andamento nesse canal"
    
    @command(
        aliases=["mw"],
        description='jogo de palavras: quem enviar mais palavras com determida sílaba vence', 
        cooldown=5,
        level="admin",
    )
    @commands.check(checks.is_admin)
    async def mostword(self, ctx):
        if not self.running.get(ctx.channel.name, False):
            pattern = self._get_pattern()
            self.running[ctx.channel.name] = {
                "checks": self._checks_wordplay,
                "update": self._update_wordplay_most,
                "pattern": pattern,
                "already": [],  # ["word1", "word2", ...]
                "longest": [None, ""],  # ["user", "longest_word"]
                "most": [None, 0],  # ["user", count]
                "players": {},  # {"user1": count, "user2": count, ...}
            }
            await ctx.send(
                f"@{ctx.author.name} iniciou um novo jogo: "
                f'envie a maior quantidade de palavras (1 por mensagem) que contiver a sílaba "{pattern.upper()}"! '
                "Acaba em 30 segundos, valendo!"
            )
            try:
                await asyncio.wait_for(
                    asyncio.sleep(60, loop=self.bot.loop), 
                    timeout=30, 
                    loop=self.bot.loop, 
                )
            except asyncio.TimeoutError:
                winner = self.running[ctx.channel.name]["most"]
                del self.running[ctx.channel.name]
                if winner[0]:
                    ctx.response = f"fim de jogo! @{winner[0]} venceu com {winner[1]} palavras 🏆"
                else:
                    ctx.response = "fim de jogo, ninguém respondeu corretamente... 👎"
            except Exception as err:
                raise err
        else:
            ctx.response = f"@{ctx.author.name}, um jogo já está em andamento nesse canal"
    
    @command(
        aliases=["hm"],
        description="jogo da forca: enviem letras para tentar descobrir qual é a palavra aleatória", 
        cooldown=2,
        level="admin",
    )
    @commands.check(checks.is_admin)
    async def hangman(self, ctx):
        if not self.running.get(ctx.channel.name, False):
            word = self._get_word().strip()
            word_ = re.sub(r"\w", "_", word)
            _id = random.randrange(0,100000)
            self.running[ctx.channel.name] = {
                "checks": self._checks_hangman,
                "update": self._update_hangman,
                "id": _id,
                "word": word,
                "corrects": {},  # {"letter1": user, "letter2": user, ...}
                "wrongs": {},  # {"letter1": user, "letter2": user, ...}
            }
            await ctx.send(
                f"@{ctx.author.name} iniciou o jogo da forca: "
                f'enviem letras até descobrirem a palavra "{word_}"! '
                f"Acaba em 2 minutos ou com 5 erros, valendo!"
            )
            try:
                await asyncio.wait_for(
                    asyncio.sleep(120, loop=self.bot.loop), 
                    timeout=120, 
                    loop=self.bot.loop, 
                )
            except asyncio.TimeoutError:
                if self.running.get(ctx.channel.name, None) and self.running[ctx.channel.name]["id"] == _id:
                    del self.running[ctx.channel.name]
                    ctx.response = "fim de jogo, ninguém descobriu a palavra a tempo... 👎"
            except Exception as err:
                raise err
        else:
            ctx.response = f"@{ctx.author.name}, um jogo já está em andamento nesse canal"

def prepare(bot):
    games = Games(bot)
    bot.add_cog(games)
    bot.add_listener(games.answers, "event_message")


def breakdown(bot):
    pass
