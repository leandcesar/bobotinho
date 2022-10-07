# -*- coding: utf-8 -*-
from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Bucket, Cog, Context, cooldown, command, helper, usage
from bobotinho.models.user import UserModel
from bobotinho.services.color import Color
from bobotinho.utils.convert import json2dict
from bobotinho.utils.time import timeago

AFKs = json2dict("bobotinho//data//afk.json")


class Stalker(Cog):
    def __init__(self, bot: Bobotinho) -> None:
        self.bot = bot
        self.color_api = Color()

    def cog_unload(self) -> None:
        self.bot.loop.create_task(self.color_api.close())

    async def cog_check(self, ctx: Context) -> bool:
        ctx.args[0] = ctx.args[0].lstrip("@").rstrip(",").lower()
        if len(ctx.args) > 1:
            ctx.args[1] = ctx.args[1].lstrip("@").rstrip(",").lower()
        return True

    @helper("saiba há quanto tempo alguém criou sua conta")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["aa", "age", "creation", "create"])
    async def accountage(self, ctx: Context, name: str = "") -> None:
        name = name or ctx.author.name

        user = await self.bot.fetch_user(name)
        if not user:
            return await ctx.reply(f"@{name} é um usuário inválido")

        mention = "você" if user.name == ctx.author.name else f"@{user.name}"
        delta = timeago(user.created_at).humanize(precision=2)
        date = user.created_at.strftime("%d/%m/%Y")
        return await ctx.reply(f"{mention} criou a conta em {date} (há {delta})")

    @helper("receba o link da foto de perfil de alguém")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["icon", "picture", "photo"])
    async def avatar(self, ctx: Context, name: str = "") -> None:
        name = name or ctx.author.name

        user = await self.bot.fetch_user(name)
        if not user:
            return await ctx.reply(f"@{name} é um usuário inválido")

        if user.name == ctx.author.name:
            return await ctx.reply(f"sua foto de perfil: {user.profile_image}")
        if user.name == self.bot.nick:
            return await ctx.reply(f"minha foto de perfil: {user.profile_image}")
        return await ctx.reply(f"foto de perfil de @{user.name}: {user.profile_image}")

    @helper("saiba a cor de alguém")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["colour", "colors"])
    async def color(self, ctx: Context, name: str = "") -> None:
        name = name or ctx.author.name
        twitch_user = await self.bot.fetch_user(name)
        if not twitch_user:
            return await ctx.reply(f"@{name} é um usuário inválido")
        user = UserModel.get_or_none(twitch_user.id)
        if not user:
            return await ctx.reply(f"@{name} ainda não foi registrado (não usou nenhum comando)")
        try:
            color_name = await self.color_api.hex_to_name(code=user.last_color)
        except Exception:
            color_name = ""
        mention = "você" if name == ctx.author.name else f"@{name}"
        colors = ", ".join(user.settings.colors) if user.settings and user.settings.colors else None
        if colors:
            return await ctx.reply(f"{mention} usa a cor {user.last_color} ({color_name}) e salvou as cores {colors}")
        return await ctx.reply(f"{mention} usa a cor {user.last_color} ({color_name})")

    @helper("saiba qual canal alguém seguiu primeiro e por quem ele foi seguido primeiro")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["ff"])
    async def firstfollow(self, ctx: Context, name: str = "", channel: str = "") -> None:
        # TODO: %firstfollow
        raise NotImplementedError()

    @helper("saiba há quanto tempo alguém segue um canal")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["fa", "followed", "follow"])
    async def followage(self, ctx: Context, name: str = "", channel: str = "") -> None:
        name = name or ctx.author.name
        channel = channel or ctx.channel.name

        user = await self.bot.fetch_user(name)
        if not user:
            return await ctx.reply(f"@{name} é um usuário inválido")

        broadcaster = await self.bot.fetch_user(channel)
        if not broadcaster:
            return await ctx.reply(f"@{channel} é um canal inválido")

        mention = "você" if user.name == ctx.author.name else f"@{user.name}"
        mention_channel = "você" if broadcaster.name == ctx.author.name else f"@{broadcaster.name}"
        if user.name == broadcaster.name:
            return await ctx.reply(f"{mention} não pode se seguir")

        try:
            follow = await user.fetch_follow(broadcaster)
            delta = timeago(follow.followed_at).humanize(precision=2)
            date = follow.followed_at.strftime("%d/%m/%Y")
            return await ctx.reply(f"{mention} seguiu {mention_channel} em {date} (há {delta})")
        except Exception:
            return await ctx.reply(f"{mention} não segue {mention_channel}")

    @helper("verifique se alguém está AFK")
    @usage("digite o comando e o nome do usuário para saber se ele está AFK")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command()
    async def isafk(self, ctx: Context, name: str) -> None:
        name = name or ctx.author.name
        if name == self.bot.nick:
            return await ctx.reply("eu sempre estou aqui... observando")
        if name == ctx.author.name:
            return await ctx.reply("você não está AFK... obviamente")
        twitch_user = await self.bot.fetch_user(name)
        if not twitch_user:
            return await ctx.reply(f"@{name} é um usuário inválido")
        user = UserModel.get_or_none(twitch_user.id)
        if not user:
            return await ctx.reply(f"@{name} ainda não foi registrado (não usou nenhum comando)")
        if user.status and not user.status.online:
            delta = timeago(user.status.updated_on).humanize(precision=2)
            action = [afk for afk in AFKs if afk["alias"] == user.status.alias][0]["isafk"]
            return await ctx.reply(f"@{name} está {action}: {user.status.message} (há {delta})")
        return await ctx.reply(f"@{name} não está AFK")

    @helper("saiba a última vez que alguém foi visto por mim")
    @usage("digite o comando e o nome de alguém para saber quando foi visto pela última vez")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["ls"])
    async def lastseen(self, ctx: Context, name: str) -> None:
        name = name or ctx.author.name
        if name == self.bot.nick:
            return await ctx.reply("eu estou em todos os lugares, a todo momento...")
        if name == ctx.author.name:
            return await ctx.reply("você foi visto pela última vez aqui ☝️")
        twitch_user = await self.bot.fetch_user(name)
        if not twitch_user:
            return await ctx.reply(f"@{name} é um usuário inválido")
        user = UserModel.get_or_none(twitch_user.id)
        if not user:
            return await ctx.reply(f"@{name} ainda não foi registrado (não usou nenhum comando)")
        delta = timeago(user.updated_on).humanize(precision=2)
        return await ctx.reply(f"@{name} foi visto em @{user.last_channel} pela última vez: {user.last_message} (há {delta})")

    @helper("veja as informações da live de algum canal")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["stream"])
    async def live(self, ctx: Context, channel: str = "") -> None:
        channel = channel or ctx.channel.name
        if channel == self.bot.nick:
            return await ctx.reply("eu sou um bot, não um streamer")

        broadcaster = await self.bot.fetch_user(name)
        if not broadcaster:
            return await ctx.reply(f"@{channel} é um canal inválido")

        try:
            data = await self.bot.fetch_streams([broadcaster.id])
            stream = data[0]
        except Exception:
            return await ctx.reply(f"@{channel} está offline")

        mention = "você" if broadcaster.name == ctx.author.name else f"@{broadcaster.name}"
        delta = timeago(stream.started_at).humanize(precision=1)
        return await ctx.reply(f"{mention} está streamando {stream.game_name} para {stream.viewer_count} viewers: {stream.title} (há {delta})")


def prepare(bot: Bobotinho) -> None:
    bot.add_cog(Stalker(bot))
