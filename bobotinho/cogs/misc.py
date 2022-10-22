# -*- coding: utf-8 -*-
from bobotinho import config
from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Bucket, Cog, Context, Message, cooldown, command, helper, usage
from bobotinho.ext.pyramid import Pyramid
from bobotinho.models.channel import ChannelModel
from bobotinho.services.discord import Discord
from bobotinho.utils.time import datetime, timeago


class Misc(Cog):
    """Miscelânea

    Comandos gerais que contém informações básicas sobre o bot
    """

    def __init__(self, bot: Bobotinho, *, session=None) -> None:
        self.bot = bot
        self.bot.listeners.insert(0, self.listener)
        self.start_time = datetime.utcnow()
        self.discord = Discord(url=config.webhook_url, session=session)
        self.pyramids: dict[str, Pyramid] = {}

    def cog_unload(self) -> None:
        self.bot.loop.create_task(self.discord.close())

    async def listener(self, ctx: Context) -> bool:
        pyramid = self.pyramids.get(ctx.channel.name, Pyramid())
        pyramid.update(ctx.author.name, ctx.message.content)
        self.pyramids[ctx.channel.name] = pyramid
        if pyramid and len(pyramid) >= 3:
            await ctx.reply(f"@{pyramid.user} fez uma pirâmide de {len(pyramid)} {pyramid.word}")
            return True
        return False

    @helper("veja as principais informações sobre o bot")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["bot", "info"])
    async def botinfo(self, ctx: Context) -> None:
        return await ctx.reply(
            f"estou conectado à {len(self.bot.connected_channels)} canais, "
            f"com {len(self.bot.commands)} comandos, "
            f"feito por @{config.dev} com TwitchIO"
        )

    @helper("reporte um bug que está ocorrendo no Bot")
    @usage("para usar: %bug <mensagem>")
    @cooldown(rate=1, per=10, bucket=Bucket.member)
    @command()
    async def bug(self, ctx: Context, *, content: str) -> None:
        user = await self.bot.fetch_user(ctx.author.name)
        avatar = user.profile_image if user else None
        if await self.discord.webhook(name=ctx.author.name, content=content, avatar=avatar):
            return await ctx.reply("seu bug foi reportado 🐛")
        return await ctx.reply("houve um erro pra registrar seu bug, tente mais tarde")

    @helper("receba o link da lista de comandos ou veja como utilizar um comando específico")
    @usage("para usar: %help <nome_do_comando>")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["commands"])
    async def help(self, ctx: Context, *, content: str = "") -> None:
        command = self.bot.get_command(content)
        if command and command.aliases:
            aliases = ", ".join([f"{ctx.prefix}{alias}" for alias in command.aliases])
            return await ctx.reply(f"{ctx.prefix}{command.name} ({aliases}): {command.description}")
        if command:
            return await ctx.reply(f"{ctx.prefix}{command.name}: {command.description}")
        return await ctx.reply(f"veja todos os comandos: {config.doc_url}")

    @helper("me adicione no seu chat")
    @command(aliases=["connect"])
    async def join(self, ctx: Context, name: str = "") -> None:
        if ctx.author.name == config.dev:
            twitch_user = await self.bot.fetch_user(name.lstrip("@").rstrip(","))
        else:
            twitch_user = await ctx.author.user()
            followers = await twitch_user.fetch_followers()
            if len(followers) < 50:
                return await ctx.reply(f"infelizmente, só posso me conectar em canais com mais de 50 seguidores")
        connected_channels = [channel.name for channel in self.bot.connected_channels]
        if twitch_user.name in connected_channels:
            if ctx.author.name == config.dev:
                return await ctx.reply(f"eu já estou conectado no chat de @{twitch_user.name}")
            return await ctx.reply(f"eu já estou conectado no seu chat")
        self.bot.channels[twitch_user.name] = ChannelModel.create(id=twitch_user.id, name=twitch_user.name, online=True)
        await self.bot._connection.send(f"JOIN #{twitch_user.name}\r\n")
        await self.discord.webhook(name=twitch_user.name, content="Adicionou o bobotinho", avatar=twitch_user.profile_image)
        if ctx.author.name == config.dev:
            return await ctx.reply(f"me conectei ao chat de @{twitch_user.name}")
        return await ctx.reply(f"me conectei ao seu chat!")

    @helper("receba o link para adicionar o bot no seu chat")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command()
    async def invite(self, ctx: Context) -> None:
        return await ctx.reply(f"basta enviar: {ctx.prefix}join")

    @helper("verifique se o bot está online")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["pong"])
    async def ping(self, ctx: Context) -> None:
        return await ctx.reply("pong 🏓")

    @helper("me reconecte ao seu chat, caso eu tenha sido banido ou algo do tipo")
    @command(aliases=["reconnect"])
    async def rejoin(self, ctx: Context, name: str = "") -> None:
        if ctx.author.name == config.dev:
            name = name.lstrip("@").rstrip(",")
        else:
            name = ctx.author.name
        if name in self.bot.channels:
            self.bot.channels[name].start()
        elif ctx.author.name == config.dev:
            return await ctx.reply(f"eu não estou conectado ao chat de @{name}, {ctx.prefix}join")
        else:
            return await ctx.reply(f"eu não estou conectado ao seu chat, use {ctx.prefix}join")
        connected_channels = [channel.name for channel in self.bot.connected_channels]
        if name in connected_channels:
            await self.bot._connection.send(f"PART #{name}\r\n")
        await self.bot._connection.send(f"JOIN #{name}\r\n")
        if ctx.author.name == config.dev:
            return await ctx.reply(f"me reconectei ao chat de @{name}")
        return await ctx.reply(f"me reconectei ao seu chat!")

    @helper("receba o link do site do Bot para mais informações")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["discord", "github", "twitter"])
    async def site(self, ctx: Context) -> None:
        return await ctx.reply(f"acesse: {config.site_url}")

    @helper("faça uma sugestão de recurso para o bot")
    @usage("para usar: %suggest <mensagem>")
    @cooldown(rate=1, per=10, bucket=Bucket.member)
    @command(aliases=["suggestion"])
    async def suggest(self, ctx: Context, *, content: str) -> None:
        user = await self.bot.fetch_user(ctx.author.name)
        avatar = user.profile_image if user else None
        if await self.discord.webhook(name=ctx.author.name, content=content, avatar=avatar):
            return await ctx.reply("sua sugestão foi anotada 💡")
        return await ctx.reply("houve um erro pra registrar sua sugestão, tente mais tarde")

    @helper("verifique há quanto tempo o bot está online")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command()
    async def uptime(self, ctx: Context) -> None:
        delta = timeago(self.start_time).humanize()
        return await ctx.reply(f"eu estou ligado há {delta}")


def prepare(bot: Bobotinho) -> None:
    bot.add_cog(Misc(bot))
