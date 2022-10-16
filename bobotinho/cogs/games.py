# -*- coding: utf-8 -*-
from collections import Counter

from bobotinho import config
from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Bucket, Cog, Context, cooldown, command, helper, usage
from bobotinho.services.dicio import Dicio
from bobotinho.services.genius import Genius
from bobotinho.services.spotify import Spotify
from bobotinho.utils.convert import str_to_ascii
from bobotinho.utils.rand import random_choice, random_number, random_line_from_txt, random_sort


class Game(Cog):
    def __init__(self, bot: Bobotinho) -> None:
        self.bot = bot
        self.channels_on_game = []
        self.dicio_api = Dicio()
        self.genius_api = Genius(key=config.genius_key)
        self.spotify_api = Spotify(client=config.spotify_client, secret=config.spotify_secret)

    def cog_unload(self) -> None:
        self.bot.loop.create_task(self.dicio_api.close())
        self.bot.loop.create_task(self.genius_api.close())
        self.bot.loop.create_task(self.spotify_api.close())

    async def cog_check(self, ctx: Context) -> bool:
        return ctx.author.is_mod or ctx.author.is_broadcaster

    @helper("jogo da forca, descubra a palavra em até 5 tentativas e 2 minutos")
    @cooldown(rate=1, per=15, bucket=Bucket.member)
    @command(aliases=["hm"])
    async def hangman(self, ctx: Context) -> None:
        if ctx.channel.name in self.channels_on_game:
            return await ctx.reply("um jogo já está em andamento nesse canal, aguarde ele finalizar")

        word = random_line_from_txt("bobotinho//data//words.txt")
        hidden_word = "".join([x if x in " -" else "_" for x in word])
        wrongs = {}  # {letter: user, ...}
        corrects = {}  # {letter: user, ...}

        try:
            self.channels_on_game.append(ctx.channel.name)
            await ctx.send(f"@{ctx.author.name} iniciou o jogo da forca, descubram a palavra: {hidden_word}")

            check = lambda message: (
                message.channel.name == ctx.channel.name
                and len(message.content) == 1
                and message.content.isalpha()
                and message.content.lower() not in corrects
                and message.content.lower() not in wrongs
            )

            while hidden_word != word:
                response = await self.bot.wait_for("message", check, timeout=30)
                message = response[0]
                letter = message.content.lower()

                if letter in word:
                    corrects[letter] = message.author.name
                else:
                    wrongs[letter] = message.author.name
                hidden_word = "".join([x if x in " -" or x in corrects else "_" for x in word])
                if letter in word:
                    await ctx.send(f"@{message.author.name} acertou, a palavra contém {letter.upper()}: {hidden_word}")
                elif len(wrongs) >= 5:
                    return await ctx.send(f"@{message.author.name} errou, a palavra não tem {letter.upper()} e acabaram as tentativas, fim de jogo!")
                else:
                    await ctx.send(f"@{message.author.name} errou, a palavra não tem {letter.upper()}, resta(m) {5 - len(wrongs)} tentativa(s): {hidden_word}")

            users = sorted(Counter(corrects.values()).items(), key=lambda x: x[1], reverse=True)
            users = ", ".join([f"@{user} ({points})" for user, points in users])
            await ctx.send(f'parabéns, a palavra "{word}" foi descoberta! 🏆 {users}')

        except Exception:
            await ctx.send("acabou o tempo, ninguém descobriu a palavra...")
        finally:
            self.channels_on_game.remove(ctx.channel.name)

    @helper("jogo da palavra mais comprida com determinada sílaba, dura 30 segundas")
    @cooldown(rate=1, per=15, bucket=Bucket.member)
    @command(aliases=["lw"])
    async def longestword(self, ctx: Context) -> None:
        if ctx.channel.name in self.channels_on_game:
            return await ctx.reply("um jogo já está em andamento nesse canal, aguarde ele finalizar")

        syllable = random_line_from_txt("bobotinho//data//syllables.txt")
        corrects = {}  # {word: user, ...}

        try:
            self.channels_on_game.append(ctx.channel.name)
            await ctx.send(f'@{ctx.author.name} iniciou o jogo, quem enviar a maior palavra com a sílaba "{syllable}" vence, valendo!')
            check = lambda message: (
                message.channel.name == ctx.channel.name
                and " " not in message.content
                and syllable in message.content.lower()
                and message.content.lower() not in corrects
                and corrects.update({message.content.lower(): message.author.name})  # add to dict (and never was True)
            )
            await self.bot.wait_for("message", check, timeout=30)
        except Exception:
            await ctx.send("fim de jogo, calculando o resultado...")
            corrects = sorted(corrects.items(), key=lambda x: len(x[0]), reverse=True)
            for word, user in corrects:
                if await self.dicio_api.exists(query=word):
                    return await ctx.send(f'@{user} venceu com a palavra "{word}" 🏆')
            else:
                await ctx.send("sem vencedores, ninguém respondeu corretamente...")
        finally:
            self.channels_on_game.remove(ctx.channel.name)

    @helper("jogo de mais palavras com determinada sílaba, dura 30 segundas")
    @cooldown(rate=1, per=15, bucket=Bucket.member)
    @command(aliases=["mw"])
    async def mostword(self, ctx: Context) -> None:
        if ctx.channel.name in self.channels_on_game:
            return await ctx.reply("um jogo já está em andamento nesse canal, aguarde ele finalizar")

        syllable = random_line_from_txt("bobotinho//data//syllables.txt")
        corrects = {}  # {word: user, ...}

        try:
            self.channels_on_game.append(ctx.channel.name)
            await ctx.send(f'@{ctx.author.name} iniciou o jogo, quem enviar mais palavras (uma por mensagem) com a sílaba "{syllable}" vence, valendo!')
            check = lambda message: (
                message.channel.name == ctx.channel.name
                and " " not in message.content
                and syllable in message.content.lower()
                and message.content.lower() not in corrects
                and corrects.update({message.content.lower(): message.author.name})  # add to dict (and never was True)
            )
            await self.bot.wait_for("message", check, timeout=30)
        except Exception:
            await ctx.send("fim de jogo, calculando o resultado...")
            corrects = {word: user for word, user in corrects.items() if await self.dicio_api.exists(query=word)}
            if corrects:
                corrects = sorted(Counter(corrects.values()).items(), key=lambda x: x[1], reverse=True)
                user = corrects[0][0]
                words = corrects[0][1]
                await ctx.send(f"@{user} venceu com {words} palavras 🏆")
            else:
                await ctx.send("sem vencedores, ninguém respondeu corretamente...")
        finally:
            self.channels_on_game.remove(ctx.channel.name)

    @helper("jogo de completar a letra da música, ganha quem fizer 5 acertos")
    @cooldown(rate=1, per=15, bucket=Bucket.member)
    @command(aliases=["gtl"])
    async def guessthelyrics(self, ctx: Context, playlist: str = "") -> None:
        if ctx.channel.name in self.channels_on_game:
            return await ctx.reply("um jogo já está em andamento nesse canal, aguarde ele finalizar")

        if "playlist/" in playlist:
            init = content.find("playlist/") + len("playlist/")
            playlist_id = content[init:]
            end = playlist_id.find("?")
            if end != -1:
                playlist_id = playlist_id[:end]
        else:
            playlist_id = "37i9dQZEVXbMXbN3EUUhlg"  # Top 50 - Brazil (by Spotify)

        no_response = 0
        corrects = {}  # {user: points, ...}

        try:
            self.channels_on_game.append(ctx.channel.name)
            songs = self.spotify_api.get_songs_from_playlist(url=playlist_id)
            songs = random_sort(songs)
            await ctx.send(f"@{ctx.author.name} iniciou o jogo, quem acertar a letra de 3 músicas primeiro vence, valendo!")

            for song in songs:
                name = song["track_name"]
                artist = song["artist_name"]
                url = song["track_url"]

                lyrics = self.genius_api.get_lyrics(title=name, artist=artist)
                if not lyrics:
                    continue

                if "chorus" in lyrics.lower():
                    i = lyrics.lower().index("chorus")
                    lines = lyrics[i + len("chorus"):].split("\n")[1:]
                elif "refrão" in lyrics.lower():
                    i = lyrics.lower().index("refrão")
                    lines = lyrics[i + len("refrão"):].split("\n")[1:]
                else:
                    lines = lyrics.split("\n")
                    i = random_number(max=len(lines))
                    lines = lines[i:]
                
                quote = ""
                for line in lines:
                    quote += f"{line} "
                    if len(quote) >= 60:
                        break
                if "[" in quote and "]" in quote:
                    quote = quote[:quote.find("[")] + quote[quote.find("]"):]
                    quote = quote.replace("  ", " ")
                quote = quote.strip()
                if not quote:
                    continue

                word = random_choice([word for word in quote.split(" ") if len(word) > 4 and word.isalpha()])
                hidden_quote = quote.replace(word, "_" * len(word), 1)

                try:
                    await ctx.send(f'Complete a letra: "{hidden_quote}"')
                    check = lambda message: (
                        message.channel.name == ctx.channel.name
                        and message.content.lower() == word.lower()
                    )
                    response = await self.bot.wait_for("message", check, timeout=20)
                    message = response[0]
                    await ctx.send(f"@{message.author.name} acertou, é a música {name} de {artist}, escute em: {url}")
                    if message.author.name in corrects:
                        corrects[message.author.name] += 1
                    else:
                        corrects[message.author.name] = 1
                    if max(corrects.values()) >= 3:
                        break
                    no_response = 0
                except Exception:
                    no_response += 1
                    await ctx.send("ninguém descobriu a letra, vamos tentar outra...")
                    if no_response >= 3:
                        break
            else:
                await ctx.send("acabaram as músicas da playlist...")

            if corrects:
                corrects = {user: points for user, points in sorted(corrects.items(), key=lambda x: x[1])}
                user = list(corrects.keys())[0]
                await ctx.send(f"fim de jogo, @{user} venceu 🏆")
            else:
                await ctx.send("fim de jogo, sem vencedores, ninguém acertou nada...")
        except Exception as e:
            raise Exception(e)
        finally:
            self.channels_on_game.remove(ctx.channel.name)


def prepare(bot: Bobotinho) -> None:
    bot.add_cog(Game(bot))
