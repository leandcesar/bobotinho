# -*- coding: utf-8 -*-
import re
from asyncio.exceptions import TimeoutError

from bobotinho.utils import checks, convert, roles

aliases = ["hm"]
description = ""
extra_checks = [roles.mod, checks.game]


async def command(ctx):
    word: str = convert.txt2randomline("bobotinho//data//words.txt")
    hidden_word: str = re.sub(r"\w", "_", word)
    wrongs: dict = {}
    corrects: dict = {}

    def play(message) -> bool:
        if len(message.content) != 1:
            return False
        if not message.content.isalpha():
            return False
        letter = message.content.lower()
        if letter in corrects or letter in wrongs:
            return False
        if letter in word:
            corrects[letter] = message.author.name
        else:
            wrongs[letter] = message.author.name
        hidden_word = "".join([x if x in corrects or x == "-" else "_" for x in word])
        if hidden_word == word:
            users: dict = {}
            for v in corrects.values():
                if v in users:
                    users[v] += 1
                else:
                    users[v] = 1
            users = sorted(users.items(), key=lambda x: x[1], reverse=True)
            users = "@" + ", @".join([f"{x[0]} ({x[1]})" for x in users])
            ctx.bot.loop.create_task(
                ctx.send(f'parabéns, a palavra "{word}" foi descoberta! 🏆 {users}')
            )
        elif letter in word:
            ctx.bot.loop.create_task(
                ctx.send(f"a palavra contém a letra {letter.upper()}: {hidden_word}")
            )
        elif len(wrongs) >= 5:
            ctx.bot.loop.create_task(
                ctx.send(
                    f"a palavra não tem a letra {letter.upper()} e "
                    f"acabaram todas as tentativas, fim de jogo!"
                )
            )
        else:
            ctx.bot.loop.create_task(
                ctx.send(
                    f"a palavra não tem a letra {letter.upper()}, "
                    f"resta(m) {5 - len(wrongs)} tentativa(s): {hidden_word}"
                )
            )
        return hidden_word == word or len(wrongs) >= 5

    def check(message) -> bool:
        if message.echo:
            return False
        if message.channel.name != ctx.channel.name:
            return False
        if not ctx.bot.channels[message.channel.name]["online"]:
            return False
        return play(message)

    try:
        ctx.response = f"você iniciou o jogo da forca, descubra a palavra em 2 minutos: {hidden_word}"
        await ctx.bot.reply(ctx)
        ctx.bot.cache.set(f"game-{ctx.channel.name}", ctx.author.name, ex=120)
        waits = ctx.bot._waiting.copy()
        await ctx.bot.wait_for("message", check, timeout=120)
    except TimeoutError:
        await ctx.send("acabou o tempo, ninguém descobriu a palavra...")
    finally:
        ctx.response = None
        ctx.bot.cache.delete(f"game-{ctx.channel.name}")
        for wait in ctx.bot._waiting:
            if wait not in waits:
                ctx.bot._waiting.remove(wait)
                break
