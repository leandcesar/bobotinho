# -*- coding: utf-8 -*-
from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Cog, Context, cooldown, command, helper, usage
from bobotinho.models.user import UserModel
from bobotinho.utils.convert import json2dict
from bobotinho.utils.rand import random_choice, random_number
from bobotinho.utils.time import timeago, timedelta

CLASSES = json2dict("bobotinho//data//classes.json")
DUNGEONS = json2dict("bobotinho//data//dungeons.json")


class Dungeon(Cog):
    def __init__(self, bot: Bobotinho) -> None:
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        if not ctx.user:
            ctx.user = UserModel.get_or_create(
                ctx.author.id,
                name=ctx.author.name,
                last_message=ctx.message.content,
                last_channel=ctx.channel.name,
                last_color=ctx.author.color,
            )
        return True

    @helper("entre na dungeon, faça sua escolha e adquira experiência")
    @cooldown(rate=1, per=30)
    @command(aliases=["ed"])
    async def enterdungeon(self, ctx: Context, *, content: str = "") -> None:
        if not ctx.user.dungeons:
            check = lambda message: (
                message.author
                and message.author.id == ctx.author.id
                and message.channel.name == ctx.channel.name
                and message.content.lower() in ("guerreiro", "arqueiro", "mago", "guerreira", "arqueira", "maga")
            )
            await ctx.reply("antes de continuar, você quer ser um guerreiro(a), arqueiro(a) ou mago(a)?")
            try:
                response = await self.bot.wait_for("message", check, timeout=60)
            except Exception:
                return None
            else:
                message = response[0]
                option = message.content.lower()
                main_class = [key for key, value in CLASSES.items() if value[0].lower() == option][0]
                ctx.user.update_dungeon(main_class=main_class)
                _class = CLASSES[ctx.user.dungeons._class][ctx.user.dungeons.level // 10]
                await ctx.reply(f"agora você é um {_class}")

        if ctx.user.dungeons.main_class and not ctx.user.dungeons.sub_class and ctx.user.dungeons.level >= 30:
            i = list(CLASSES).index(ctx.user.dungeons.main_class)
            class_1 = CLASSES[list(CLASSES)[i]]
            class_2 = CLASSES[list(CLASSES)[i + 1]]
            options = (class_1[3], class_2[3])
            check = lambda message: (
                message.author
                and message.author.id == ctx.author.id
                and message.channel.name == ctx.channel.name
                and message.content.lower() in options
            )
            await ctx.reply(f"antes de continuar, você deve escolher sua nova classe: {options[0]} ou {options[1]}?")
            try:
                response = await self.bot.wait_for("message", check, timeout=60)
            except Exception:
                return None
            else:
                message = response[0]
                option = message.content.lower()
                main_class = [key for key, value in CLASSES.items() if value[3].lower() == option][0]
                ctx.user.update_dungeon(main_class=main_class)
                _class = CLASSES[ctx.user.dungeons._class][ctx.user.dungeons.level // 10]
                await ctx.reply(f"agora você é um {_class}")

        if (
            timeago(ctx.user.dungeons.updated_on).total_in_seconds() < 10800
            and ctx.user.dungeons.created_on.isoformat()[:18] != ctx.user.dungeons.updated_on.isoformat()[:18]
        ):
            delta = timeago(ctx.user.dungeons.updated_on + timedelta(seconds=10800), reverse=True)
            return await ctx.reply(f"aguarde {delta.humanize(precision=2, short=True)} para entrar em outra dungeon ⌛")

        i = random_number(min=0, max=len(DUNGEONS))
        dungeon = DUNGEONS[i]
        check = lambda message: (
            message.author
            and message.author.id == ctx.author.id
            and message.channel.name == ctx.channel.name
            and message.content.lower() in ("1", "2", f"{self.bot._prefix}ed 1", f"{self.bot._prefix}ed 2")
        )
        await ctx.reply(f'{dungeon["quote"]} você quer {dungeon["1"]["option"]} ou {dungeon["2"]["option"]}? (1 ou 2)')
        try:
            response = await self.bot.wait_for("message", check, timeout=60)
        except Exception:
            return None
        else:
            message = response[0]
            option = message.content.lower().replace(f"{self.bot._prefix}ed ", "")

        result = random_choice(["win", "lose"])
        if result == "win":
            experience = int(random_number(min=50, max=75) + 3 * ctx.user.dungeons.level)
            if ctx.user.dungeons.experience + experience > 100 * (ctx.user.dungeons.level) + 25 * sum(range(1, ctx.user.dungeons.level + 1)):
                ctx.user.update_dungeon(win=True, experience=experience, level_up=True)
                return await ctx.reply(f"{dungeon[option][result]}! +{experience} XP e alcançou level {ctx.user.dungeons.level} ⬆")
            else:
                ctx.user.update_dungeon(win=True, experience=experience)
                return await ctx.reply(f"{dungeon[option][result]}! +{experience} XP")
        else:
            ctx.user.update_dungeon(defeat=True)
            return await ctx.reply(f"{dungeon[option][result]}! +0 XP")

    @helper("entre na dungeon e adquira experiência sem precisar tomar uma escolha")
    @cooldown(rate=1, per=30)
    @command(aliases=["fed", "fd"])
    async def fastdungeon(self, ctx: Context) -> None:
        if not ctx.user.dungeons:
            check = lambda message: (
                message.author
                and message.author.id == ctx.author.id
                and message.channel.name == ctx.channel.name
                and message.content.lower() in ("guerreiro", "arqueiro", "mago", "guerreira", "arqueira", "maga")
            )
            await ctx.reply("antes de continuar, você quer ser um guerreiro(a), arqueiro(a) ou mago(a)?")
            try:
                response = await self.bot.wait_for("message", check, timeout=60)
            except Exception:
                return None
            else:
                message = response[0]
                option = message.content.lower()
                main_class = [key for key, value in CLASSES.items() if value[0].lower() == option][0]
                ctx.user.update_dungeon(main_class=main_class)
                _class = CLASSES[ctx.user.dungeons._class][ctx.user.dungeons.level // 10]
                await ctx.reply(f"agora você é um {_class}")

        if ctx.user.dungeons.main_class and not ctx.user.dungeons.sub_class and ctx.user.dungeons.level >= 30:
            i = list(CLASSES).index(ctx.user.dungeons.main_class)
            class_1 = CLASSES[list(CLASSES)[i]]
            class_2 = CLASSES[list(CLASSES)[i + 1]]
            options = (class_1[3], class_2[3])
            check = lambda message: (
                message.author
                and message.author.id == ctx.author.id
                and message.channel.name == ctx.channel.name
                and message.content.lower() in options
            )
            await ctx.reply(f"antes de continuar, você deve escolher sua nova classe: {options[0]} ou {options[1]}?")
            try:
                response = await self.bot.wait_for("message", check, timeout=60)
            except Exception:
                return None
            else:
                message = response[0]
                option = message.content.lower()
                main_class = [key for key, value in CLASSES.items() if value[3].lower() == option][0]
                ctx.user.update_dungeon(main_class=main_class)
                _class = CLASSES[ctx.user.dungeons._class][ctx.user.dungeons.level // 10]
                await ctx.reply(f"agora você é um {_class}")

        if (
            timeago(ctx.user.dungeons.updated_on).total_in_seconds() < 10800
            and ctx.user.dungeons.created_on.isoformat()[:18] != ctx.user.dungeons.updated_on.isoformat()[:18]
        ):
            delta = timeago(ctx.user.dungeons.updated_on + timedelta(seconds=10800), reverse=True)
            return await ctx.reply(f"aguarde {delta.humanize(precision=2, short=True)} para entrar em outra dungeon ⌛")

        i = random_number(min=0, max=len(DUNGEONS))
        dungeon = DUNGEONS[i]
        option = random_choice(["1", "2"])
        result = random_choice(["win", "lose"])
        quote = f'{dungeon["quote"]} você decide {dungeon[option]["option"]}'
        if result == "win":
            experience = int(random_number(min=50, max=75) + 3 * ctx.user.dungeons.level)
            if ctx.user.dungeons.experience + experience > 100 * (ctx.user.dungeons.level) + 25 * sum(range(1, ctx.user.dungeons.level + 1)):
                ctx.user.update_dungeon(win=True, experience=experience, level_up=True)
                return await ctx.reply(f"{quote} e {dungeon[option][result]}! +{experience} XP e alcançou level {ctx.user.dungeons.level} ⬆")
            else:
                ctx.user.update_dungeon(win=True, experience=experience)
                return await ctx.reply(f"{quote} e {dungeon[option][result]}! +{experience} XP")
        else:
            ctx.user.update_dungeon(defeat=True)
            return await ctx.reply(f"{quote} e {dungeon[option][result]}! +0 XP")

    @helper("veja qual o seu level (ou de alguém) e outras estatísticas da dungeon")
    @cooldown(rate=3, per=10)
    @command(aliases=["lvl"])
    async def level(self, ctx: Context, name: str = "") -> None:
        name = name or ctx.author.name
        if name == self.bot.nick:
            return await ctx.reply("eu apenas crio as dungeons...")
        twitch_user = await self.bot.fetch_user(name)
        if not twitch_user:
            return await ctx.reply(f"@{name} é um usuário inválido")
        user = UserModel.get_or_none(twitch_user.id)
        if not user:
            return await ctx.reply(f"@{name} ainda não foi registrado (não usou nenhum comando)")
        mention = "você" if name == ctx.author.name else f"@{name}"
        if user.dungeons:
            _class = CLASSES[ctx.user.dungeons._class][ctx.user.dungeons.level // 10]
            winrate = user.dungeons.wins / (user.dungeons.total or 1) * 100
            return await ctx.reply(
                f"{mention} é {_class} (LVL {user.dungeons.level}), com {user.dungeons.total} dungeons "
                f"({user.dungeons.wins} vitórias, {user.dungeons.defeats} derrotas, {winrate:.2f}% winrate) ♦"
            )
        return await ctx.reply(f"{mention} ainda não entrou em nenhuma dungeon")

    @helper("saiba quais são os melhores jogadores da dungeon")
    @cooldown(rate=3, per=10)
    @command()
    async def rank(self, ctx: Context, order_by: str = "") -> None:
        # TODO
        raise NotImplementedError()


def prepare(bot: Bobotinho) -> None:
    bot.add_cog(Dungeon(bot))
