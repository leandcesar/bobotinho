# -*- coding: utf-8 -*-
from asyncio import TimeoutError

from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Cog, Context, cooldown, command, helper, usage
from bobotinho.utils.convert import str2int
from bobotinho.utils.rand import random_choice


class Interact(Cog):
    def __init__(self, bot: Bobotinho) -> None:
        self.bot = bot
        self.fights = {}

    async def cog_check(self, ctx: Context) -> bool:
        ctx.args[0] = ctx.args[0].lstrip("@").rstrip(",").lower()
        if len(ctx.args) > 1:
            ctx.args[1] = ctx.args[1].lstrip("@").rstrip(",").lower()
        return True

    @helper("desafie alguém para lutar")
    @usage("digite o comando e o nome de alguém para desafiá-lo para luta")
    @cooldown(rate=3, per=10)
    @command()
    async def fight(self, ctx: Context, name: str) -> None:
        if name == self.bot.nick:
            return await ctx.reply("você nunca conseguiria me derrotar...")
        if name == ctx.author.name:
            return await ctx.reply("você iniciou uma luta interna...")
        if self.fights.get(name):
            return await ctx.reply(f"@{name} já está sendo desafiado por @{self.fights[name]}")

        try:
            self.fights[name] = ctx.author.name
            check = lambda message: (
                message.author
                and message.author.name == name
                and message.channel.name == ctx.channel.name
                and message.content.lower() in ("sim", "s", "não", "nao", "n")
            )
            await ctx.reply(f"desafiou @{name} para uma luta! @{name} você aceita? (sim/não)")
            response = await self.bot.wait_for("message", check, timeout=30)
            message = response[0]
            if message.content.lower() in ("sim", "s"):
                result = random_choice(
                    [
                        f"@{name} acaba com {ctx.author.name}!",
                        f"@{name} deixa {ctx.author.name} desacordado!",
                        f"@{name} derrota {ctx.author.name} facilmente!",
                        f"@{name} espanca {ctx.author.name} sem piedade!",
                        f"@{name} não dá chances para {ctx.author.name} e vence!",
                        f"@{name} quase perde, mas derruba {ctx.author.name}!",
                        f"@{name} vence a luta contra {ctx.author.name}!",
                        f"@{name} vence {ctx.author.name} com dificuldades!",
                        f"@{name} vence {ctx.author.name} em uma luta acirrada!",
                        f"@{name} vence {ctx.author.name} facilmente!",
                        f"@{ctx.author.name} acaba com {name}!",
                        f"@{ctx.author.name} deixa {name} desacordado!",
                        f"@{ctx.author.name} derrota {name} facilmente!",
                        f"@{ctx.author.name} espanca {name} sem piedade!",
                        f"@{ctx.author.name} não dá chances para {name} e vence!",
                        f"@{ctx.author.name} quase perde, mas derruba {name}!",
                        f"@{ctx.author.name} vence a luta contra {name}!",
                        f"@{ctx.author.name} vence {name} com dificuldades!",
                        f"@{ctx.author.name} vence {name} em uma luta acirrada!",
                        f"@{ctx.author.name} vence {name} facilmente!",
                    ]
                )
                await ctx.send(result)
            elif message.content.lower() in ("não", "nao", "n"):
                await ctx.send(f"@{name} recusou o desafio contra @{ctx.author.name} LUL")
        except TimeoutError:
            pass
        finally:
            self.fights.pop(name)

    @helper("dê um abraço em alguém do chat")
    @usage("digite o comando e o nome de alguém para abracá-lo")
    @cooldown(rate=3, per=10)
    @command()
    async def hug(self, ctx: Context, name: str) -> None:
        if name == self.bot.nick:
            return await ctx.reply("🤗")
        if name == ctx.author.name:
            return await ctx.reply("você tentou se abraçar...")
        return await ctx.reply(f"você abraçou @{name} 🤗")

    @helper("dê um beijinho em alguém do chat")
    @usage("digite o comando e o nome de alguém para beijá-lo")
    @cooldown(rate=3, per=10)
    @command()
    async def kiss(self, ctx: Context, name: str) -> None:
        if name == self.bot.nick:
            return await ctx.reply("😳")
        if name == ctx.author.name:
            return await ctx.reply("você tentou se beijar...")
        return await ctx.reply(f"você deu um beijinho em @{name} 😚")

    @helper("veja quanto de amor existe entre o ship de duas pessoas")
    @usage("digite o comando e o nome de uma ou duas pessoas")
    @cooldown(rate=3, per=10)
    @command(aliases=["ship"])
    async def love(self, ctx: Context, name1: str, name2: str = "") -> None:
        if not name2:
            name1, name2 = ctx.author.name, name1
        if name1 == name2:
            return await ctx.reply("uma pessoa não pode ser shipada com ela mesma...")

        ship = name1[:len(name1)//2 + 1] + name2[len(name2)//2 + 1:]
        percentage = str2int(ship) % 101

        if ship in ("pchantinho", "discretre"):  # it's love, not manipulation
            percentage = 100

        emojis = ["😭", "😥", "💔", "😢", "😐", "😊", "❤", "💕", "💘", "😍", "PogChamp ❤"]
        emoji = emojis[round(percentage / 10)]
        return await ctx.reply(f"@{name1} & @{name2}: {ship} com {percentage}% de amor {emoji}")

    @helper("faça carinho em alguém do chat")
    @usage("digite o comando e o nome de alguém para fazer carinho")
    @cooldown(rate=3, per=10)
    @command()
    async def pat(self, ctx: Context, name: str) -> None:
        if name == self.bot.nick:
            return await ctx.reply("😊")
        if name == ctx.author.name:
            return await ctx.reply("você tentou fazer cafuné em si mesmo...")
        return await ctx.reply(f"você fez cafuné em @{name} 😊")

    @helper("é... é isso mesmo")
    @usage("digite o comando e o nome de alguém para ver o tamanho do p")
    @cooldown(rate=3, per=10)
    @command()
    async def penis(self, ctx: Context, name: str = "") -> None:
        name = name or ctx.author.name
        if name == self.bot.nick:
            return await ctx.reply("eu só tenho pen drive")
        length = str2int(name) % 28 + 5
        emoji = "🤏" if length <= 13 else "🍌" if length <= 19 else "🍆"
        mention = "você" if name == ctx.author.name else f"@{name}"
        return await ctx.reply(f"{mention} tem {length}cm {emoji}")

    @helper("dê um tapa em alguém do chat")
    @usage("digite o comando e o nome de alguém que mereça levar uns tapas")
    @cooldown(rate=3, per=10)
    @command()
    async def slap(self, ctx: Context, name: str) -> None:
        if name == self.bot.nick:
            return await ctx.reply("vai bater na mãe 😠")
        if name == ctx.author.name:
            return await ctx.reply("você se deu um tapa... 😕")
        return await ctx.reply(f"você deu um tapa em @{name} 👋")

    @helper("coloque alguém do chat na cama para dormir")
    @usage("digite o comando e o nome de alguém para colocá-lo na cama")
    @cooldown(rate=3, per=10)
    @command()
    async def tuck(self, ctx: Context, name: str) -> None:
        if name == self.bot.nick:
            return await ctx.reply("eu não posso dormir agora...")
        if name == ctx.author.name:
            return await ctx.reply("você foi para a cama")
        return await ctx.reply(f"você colocou @{name} na cama 🙂👉🛏")


def prepare(bot: Bobotinho) -> None:
    bot.add_cog(Interact(bot))
