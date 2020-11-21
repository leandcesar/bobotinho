# -*- coding: utf-8 -*-

from ext.command import command
from twitchio.ext import commands
from utils import convert, checks


class Admin(commands.AutoCog):
    def __init__(self, bot):
        self.bot = bot

    def _prepare(self, bot):
        pass

    async def _change_disabled(self, ctx, command: str):
        command = convert.command(command)
        disable = ctx.command.name == "disable"
        action = "desativado" if disable else "ativado"
        operation = "+" if disable else "-"

        if not command in [c.name for c in self.bot.commands.values()]:
            return f"@{ctx.author.name}, esse comando não existe"
        elif disable and self.bot.commands[command].level in ("admin", "owner"):
            return (
                f"@{ctx.author.name}, {ctx.prefix}{command} não pode ser {action}"
            )
        elif disable == self.bot.channels.is_disabled(ctx.channel.name, command):
            return f"@{ctx.author.name}, {ctx.prefix}{command} já está {action}"
        else:
            self.bot.channels[ctx.channel.name].disabled = operation + command
            await self.bot.db.update(
                "channels",
                values={"disabled": self.bot.channels[ctx.channel.name].disabled},
                where={"name": ctx.channel.name},
            )
            return f"@{ctx.author.name}, {ctx.prefix}{command} foi {action}"

    async def _change_status(self, ctx, value: bool):
        self.bot.channels[ctx.channel.name].status = value
        await self.bot.db.update(
            "channels", values={"status": value}, where={"name": ctx.channel.name}
        )

    @command(
        level="admin",
        description="desative um comando",
        cooldown=2,
        usage="digite o comando e o nome do comando que quer desativar",
    )
    @commands.check(checks.is_admin)
    async def disable(self, ctx, command: str):
        ctx.response = await self._change_disabled(ctx, command)

    @command(
        level="admin",
        description="reative um comando",
        cooldown=2,
        usage="digite o comando e o nome do comando que quer reativar",
    )
    @commands.check(checks.is_admin)
    async def enable(self, ctx, command: str):
        ctx.response = await self._change_disabled(ctx, command)

    @command(level="admin", description="despause o bot", cooldown=10)
    @commands.check(checks.is_admin)
    async def start(self, ctx):
        await self._change_status(ctx, True)
        ctx.response = f"@{ctx.author.name} me ligou ☕"

    @command(level="admin", description="pause o bot", cooldown=10)
    @commands.check(checks.is_admin)
    async def stop(self, ctx):
        await self._change_status(ctx, False)
        ctx.response = f"@{ctx.author.name} me desligou 💤"


def prepare(bot):
    bot.add_cog(Admin(bot))


def breakdown(bot):
    pass
