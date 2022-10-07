# -*- coding: utf-8 -*-
from bobotinho import config
from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Cog, Context, command, helper, usage
from bobotinho.models.channel import ChannelModel


class Settings(Cog):
    def __init__(self, bot: Bobotinho) -> None:
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        if ctx.args:
            ctx.args[0] = ctx.args[0].lstrip("@").rstrip(",").lower().strip()
        return ctx.author.is_mod or ctx.author.is_broadcaster or ctx.author.name == config.dev

    @helper("ative um comando")
    @usage("digite o comando e o nome de um comando")
    @command()
    async def enable(self, ctx: Context, name: str) -> None:
        command = self.bot.get_command(name)
        if not command:
            return await ctx.reply("esse comando não existe")
        if self.bot.channels[ctx.channel.name].enable_command(command.name):
            return await ctx.reply(f'"{command.name}" foi ativado')
        return await ctx.reply(f'"{command.name}" já está ativado')

    @helper("desative um comando")
    @usage("digite o comando e o nome de um comando")
    @command()
    async def disable(self, ctx: Context, name: str) -> None:
        command = self.bot.get_command(name)
        if not command:
            return await ctx.reply("esse comando não existe")
        if command.cog.name == self.name:
            return await ctx.reply(f'"{command.name}" não pode ser desativado')
        if self.bot.channels[ctx.channel.name].disable_command(command.name):
            return await ctx.reply(f'"{command.name}" foi desativado')
        return await ctx.reply(f'"{command.name}" já está desativado')

    @helper("despause o bot")
    @command(no_global_checks=True)
    async def start(self, ctx: Context) -> None:
        if self.bot.channels[ctx.channel.name].start():
            return await ctx.reply("você me ligou ☕")
        return await ctx.reply("já estou ligado ☕")

    @helper("pause o bot")
    @command()
    async def stop(self, ctx: Context) -> None:
        if self.bot.channels[ctx.channel.name].stop():
            return await ctx.reply("você me desligou 💤")

    @helper("me adicione no seu chat")
    @command()
    async def join(self, ctx: Context, name: str = "") -> None:
        if ctx.author.name == config.dev:
            twitch_user = await self.bot.fetch_user(name)
        else:
            twitch_user = await ctx.author.user()
        if not twitch_user:
            return await ctx.reply(f"@{name} é um usuário inválido")
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
        if ctx.author.name == config.dev:
            return await ctx.reply(f"me conectei ao chat de @{twitch_user.name}")
        return await ctx.reply(f"me conectei ao seu chat!")


def prepare(bot: Bobotinho) -> None:
    bot.add_cog(Settings(bot))
