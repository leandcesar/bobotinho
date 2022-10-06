# -*- coding: utf-8 -*-
from bobotinho import config
from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Cog, Context, Message, cooldown, command, helper, usage
from bobotinho.ext.pyramid import Pyramid
from bobotinho.services.discord import Discord
from bobotinho.utils.time import datetime, timeago


class Misc(Cog):
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
    @cooldown(rate=3, per=10)
    @command(aliases=["bot", "info"])
    async def botinfo(self, ctx: Context) -> None:
        return await ctx.reply(
            f"estou conectado à {len(self.bot.connected_channels)} canais, "
            f"com {len(self.bot.commands)} comandos, "
            f"feito por @{config.dev} com TwitchIO"
        )

    @helper("reporte um bug que está ocorrendo no Bot")
    @usage("digite o comando e o bug que você encontrou")
    @cooldown(rate=1, per=10)
    @command()
    async def bug(self, ctx: Context, *, content: str) -> None:
        user = await self.bot.fetch_user(ctx.author.name)
        avatar = user.profile_image if user else None
        if await self.discord.webhook(name=ctx.author.name, content=content, avatar=avatar):
            return await ctx.reply("seu bug foi reportado 🐛")
        return await ctx.reply("houve um erro pra registrar seu bug, tente mais tarde")

    @helper("receba o link da lista de comandos ou veja como utilizar um comando específico")
    @cooldown(rate=3, per=10)
    @command(aliases=["commands"])
    async def help(self, ctx: Context, *, content: str = None) -> None:
        command = self.bot.get_command(content)
        if command and command.aliases:
            aliases = ", ".join([f"{ctx.prefix}{alias}" for alias in command.aliases])
            return await ctx.reply(f"{ctx.prefix}{command.name} ({aliases}): {command.description}")
        if command:
            return await ctx.reply(f"{ctx.prefix}{command.name}: {command.description}")
        return await ctx.reply(f"veja todos os comandos: {config.doc_url}")

    @helper("receba o link para adicionar o bot no seu chat")
    @cooldown(rate=3, per=10)
    @command()
    async def invite(self, ctx: Context) -> None:
        return await ctx.reply(f"me adicione no seu chat: {config.invite_url}")

    @helper("verifique se o bot está online")
    @cooldown(rate=3, per=10)
    @command(aliases=["pong"])
    async def ping(self, ctx: Context) -> None:
        return await ctx.reply("pong 🏓")

    @helper("receba o link do site do Bot para mais informações")
    @cooldown(rate=3, per=10)
    @command(aliases=["discord", "github", "twitter"])
    async def site(self, ctx: Context) -> None:
        return await ctx.reply(f"acesse: {config.site_url}")

    @helper("faça uma sugestão de recurso para o bot")
    @usage("digite o comando e uma sugestão de recurso ou modificação para o bot")
    @cooldown(rate=1, per=10)
    @command(aliases=["suggestion"])
    async def suggest(self, ctx: Context, *, content: str) -> None:
        user = await self.bot.fetch_user(ctx.author.name)
        avatar = user.profile_image if user else None
        if await self.discord.webhook(name=ctx.author.name, content=content, avatar=avatar):
            return await ctx.reply("sua sugestão foi anotada 💡")
        return await ctx.reply("houve um erro pra registrar sua sugestão, tente mais tarde")

    @helper("verifique há quanto tempo o bot está online")
    @cooldown(rate=3, per=10)
    @command()
    async def uptime(self, ctx: Context) -> None:
        delta = timeago(self.start_time).humanize()
        return await ctx.reply(f"eu estou ligado há {delta}")


def prepare(bot: Bobotinho) -> None:
    bot.add_cog(Misc(bot))
