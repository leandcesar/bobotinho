# -*- coding: utf-8 -*-
from bobotinho import config
from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Cog, Context, command, helper, usage


class Settings(Cog):
    """Administração

    Comandos para os moderadores do canal controlarem o bot
    """

    def __init__(self, bot: Bobotinho) -> None:
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        return ctx.author.is_mod or ctx.author.is_broadcaster or ctx.author.name == config.dev

    @helper("ative um comando")
    @usage("para usar: %enable <nome_do_comando>")
    @command()
    async def enable(self, ctx: Context, name: str) -> None:
        command = self.bot.get_command(name.lower().strip())
        if not command:
            return await ctx.reply("esse comando não existe")
        if self.bot.channels[ctx.channel.name].enable_command(command.name):
            return await ctx.reply(f'"{command.name}" foi ativado')
        return await ctx.reply(f'"{command.name}" já está ativado')

    @helper("desative um comando")
    @usage("para usar: %disable <nome_do_comando>")
    @command()
    async def disable(self, ctx: Context, name: str) -> None:
        command = self.bot.get_command(name.lower().strip())
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


def prepare(bot: Bobotinho) -> None:
    bot.add_cog(Settings(bot))
