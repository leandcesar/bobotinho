# -*- coding: utf-8 -*-
from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Bucket, Cog, Context, cooldown, command, helper, usage
from bobotinho.utils.convert import json_to_dict
from bobotinho.utils.rand import random_sort
from bobotinho.utils.time import datetime

PETS = json_to_dict("bobotinho//data//pets.json")


class Pet(Cog):
    def __init__(self, bot: Bobotinho) -> None:
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        if ctx.args and isinstance(ctx.args[0], str):
            ctx.args[0] = ctx.args[0].lstrip("@").rstrip(",").lower()
        return True

    @staticmethod
    def _petlist(*, limit: int = 6) -> list[dict]:
        seed = datetime.utcnow().toordinal()
        pets = random_sort(list(PETS.copy().values()), seed=seed)
        pets = list(sorted(pets[:limit], key=lambda k: k["price"]))
        return pets

    @helper("veja os pets de alguém")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["pets"])
    async def pet(self, ctx: Context, name: str = "") -> None:
        name = name or ctx.author.name
        if name == self.bot.nick:
            return await ctx.reply("eu tenho todos os pets, e ofereço alguns pra vocês")
        if name == ctx.author.name:
            user = ctx.user
        else:
            user = await self.bot.fetch_user_db(name)
            if not user:
                return await ctx.reply(f"@{name} ainda não foi registrado (não usou nenhum comando)")
        if user.settings and not user.settings.mention:
            return await ctx.reply("esse usuário optou por não permitir ser mencionado")
        mention = "você" if name == ctx.author.name else f"@{name}"
        if user.pets:
            pets = " ".join([f'{pet} {PETS[pet.specie]["emoji"]}' for pet in user.pets])
            return await ctx.reply(f"{mention} possui {pets}")
        if name == ctx.author.name:
            return await ctx.reply(f"adquira um dos pets disponíveis ({ctx.prefix}petlist) em troca de cookies")
        return await ctx.reply(f"{mention} não possui nenhum pet")

    @helper("adquira um dos pets disponíveis na loja")
    @usage("digite o comando e um dos pets disponíveis (%petlist) para adquirí-lo")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command()
    async def petbuy(self, ctx: Context, specie: str) -> None:
        if ctx.user.pets and len(ctx.user.pets) >= 3:
            return await ctx.reply(f"você já possui a quantidade máxima de pets")
        if not ctx.user.cookies:
            return await ctx.reply(f"comece a estocar cookies para adquirir um pet ({ctx.prefix}stock)")
        for pet in self._petlist():
            if pet["specie"] == specie.lower():
                price = pet["price"]
                emoji = pet["emoji"]
                if ctx.user.cookies.stocked < price:
                    return await ctx.reply(f"estoque {price} cookies para adquirir {specie}")
                if ctx.user.update_cookie(consume=price):
                    ctx.user.add_pet(specie=specie)
                    return await ctx.reply(f"você adquiriu {specie} {emoji} por {price} cookies, agora dê um nome ({ctx.prefix}petname)")
        else:
            return await ctx.reply(f"escolha um dos pets disponíveis hoje ({ctx.prefix}petlist)")

    @helper("dê um nome para o seu pet")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command()
    async def petname(self, ctx: Context) -> None:
        if not ctx.user.pets:
            return await ctx.reply("você não tem pets para dar nome")
        if len(ctx.user.pets) > 1:
            pets = [f"{pet}" for pet in ctx.user.pets]
            numbers = [f"{x + 1}" for x in range(len(pets))]
            check = lambda message: (
                message.author
                and message.author.id == ctx.author.id
                and message.channel.name == ctx.channel.name
                and message.content.lower() in (pets + numbers)
            )
            pets_str = ", ".join(pets)
            numbers_str = "/".join(numbers)
            await ctx.reply(f"qual dos pets você quer nomear: {pets_str} ({numbers_str})?")
            try:
                response = await self.bot.wait_for("message", check, timeout=30)
            except Exception:
                return None
            else:
                message = response[0]
                option = message.content.lower()
                if option in numbers:
                    option = pets[int(option) - 1]
                pet = [pet for pet in ctx.user.pets if f"{pet}" == option][0]
        else:
            pet = ctx.user.pets[0]
        check = lambda message: (
            message.author
            and message.author.id == ctx.author.id
            and message.channel.name == ctx.channel.name
        )
        await ctx.reply(f"qual nome você quer dar para {pet}?")
        try:
            response = await self.bot.wait_for("message", check, timeout=60)
        except Exception:
            return None
        else:
            message = response[0]
            name = message.content.split()[0][:32]
            ctx.user.update_pet(pet, name=name)
            await ctx.reply(f"agora você tem um pet chamado {name}")

    @helper("faça carinho nos seus pets")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command()
    async def petpat(self, ctx: Context) -> None:
        if ctx.user.pets:
            pets = " ".join([f'{pet} {PETS[pet.specie]["emoji"]}' for pet in ctx.user.pets])
            return await ctx.reply(f"você fez carinho em {pets}")
        return await ctx.reply(f"adquira um dos pets disponíveis ({ctx.prefix}petlist) em troca de cookies")

    @helper("devolva um pet em troca de parte da quantia que gastou")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command()
    async def petsell(self, ctx: Context) -> None:
        if not ctx.user.pets:
            return await ctx.reply("você não tem pets para vender")
        if len(ctx.user.pets) > 1:
            pets = [f"{pet}" for pet in ctx.user.pets]
            numbers = [f"{x + 1}" for x in range(len(pets))]
            check = lambda message: (
                message.author
                and message.author.id == ctx.author.id
                and message.channel.name == ctx.channel.name
                and message.content.lower() in (pets + numbers)
            )
            pets_str = ", ".join(pets)
            numbers_str = "/".join(numbers)
            await ctx.reply(f"qual dos pets você quer vender: {pets_str} ({numbers_str})?")
            try:
                response = await self.bot.wait_for("message", check, timeout=30)
            except Exception:
                return None
            else:
                message = response[0]
                option = message.content.lower()
                if option in numbers:
                    option = pets[int(option) - 1]
                pet = [pet for pet in ctx.user.pets if f"{pet}" == option][0]
        else:
            pet = ctx.user.pets[0]
            check = lambda message: (
                message.author
                and message.author.id == ctx.author.id
                and message.channel.name == ctx.channel.name
                and message.content.lower() in ("sim", "s", "não", "nao","n")
            )
            await ctx.reply(f"tem certeza que você quer vender {pet}?")
            try:
                response = await self.bot.wait_for("message", check, timeout=30)
            except Exception:
                return None
            else:
                message = response[0]
                option = message.content.lower()
                if option.startswith("n"):
                    return await ctx.reply("boa escolha")
        price = PETS[pet.specie]["price"]
        earnings = price // 2
        ctx.user.remove_pet(pet)
        if ctx.user.update_cookie(earnings=earnings):
            return await ctx.reply(f"você se livrou do seu pet e recebeu {earnings} cookies, parabéns, você é um péssimo ser humano!")

    @helper("veja os pets disponíveis para adquirir")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command()
    async def petlist(self, ctx: Context) -> None:
        pets = ", ".join([f'{pet["specie"]} ({pet["price"]})' for pet in self._petlist()])
        return await ctx.reply(f"pets disponíveis (adquira com {ctx.prefix}petbuy): {pets}")


def prepare(bot: Bobotinho) -> None:
    bot.add_cog(Pet(bot))
