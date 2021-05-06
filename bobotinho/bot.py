# -*- coding: utf-8 -*-
from bobotinho.autobot import AutoBot, CheckFailure, CommandNotFound, MissingRequiredArgument
from bobotinho.database import models
from bobotinho.logger import log
from bobotinho.utils import checks


class Bobotinho(AutoBot):
    def __init__(self, config, loop=None):
        super().__init__(
            irc_token=config.irc_token,
            client_id=config.client_id,
            client_secret=config.client_secret,
            prefix=config.prefix,
            nick=config.nick,
            loop=loop,
        )
        self.site = config.site
        self.owner = config.owner
        self.cache = {}

    async def add_all_channels(self):
        self.channels = {
            channel.user_id: {
                "banwords": list(channel.banwords.keys()),
                "disabled": list(channel.disabled.keys()),
                "status": channel.status,
            } for channel in await models.Channel.all()
        }
        failed = await self.join_all_channels(list(self.channels.keys()))
        for fail in failed:
            self.channels.pop(fail)

    async def event_ready(self):
        self.add_all_commands()
        self.add_all_listeners()
        self.add_all_tasks()
        self.add_all_checks([checks.is_online, checks.is_enabled, checks.is_cooldown])
        await self.add_all_channels()
        log.info(f"{self.nick} | #{len(self.channels)} | {self.prefixes[0]}{len(self.commands)}")

    async def event_error(self, e, data=None):
        log.exception(e)

    async def event_command_error(self, ctx, e):
        if isinstance(e, CheckFailure) and str(e).split()[-1] == "is_enabled":
            ctx.response = "esse comando está desativado nesse canal"
        elif isinstance(e, CheckFailure) and str(e).split()[-1] == "is_banword":
            ctx.response = "sua mensagem contém algum termo banido desse canal"
        elif isinstance(e, CheckFailure) and str(e).split()[-1] == "is_allowed":
            ctx.response = "apenas inscritos, VIPs e moderadores podem utilizar links"
        elif isinstance(e, MissingRequiredArgument) and ctx.command.usage:
            ctx.response = ctx.command.usage
        elif isinstance(e, (CheckFailure, CommandNotFound)):
            log.error(e)
        else:
            log.exception(e)

    async def global_before_hook(self, ctx):
        log.info(f"#{ctx.channel.name} @{ctx.author.name}: {ctx.content}")
        ctx.command.invocation = ctx.content.partition(" ")[0][len(ctx.prefix):]
        ctx.prefix = self.prefixes[0]
        await models.User.update_or_create_from_ctx(ctx)

    async def global_after_hook(self, ctx):
        if not hasattr(ctx, "response") and ctx.command.usage:
            log.error(f'"{ctx.content}" has no ctx.response from #{ctx.channel.name}')
            ctx.response = ctx.command.usage
        elif not hasattr(ctx, "response"):
            log.error(f'"{ctx.content}" has no ctx.response from #{ctx.channel.name}')
            ctx.response = "ocorreu um erro inesperado"
        elif len(ctx.response) > 400:
            log.error(f'"{ctx.response}" > 400 characters')
            ctx.response = "esse comando gerou uma resposta muito grande"
        response = f"@{ctx.author.name}, {ctx.response}"
        await ctx.send(response)
        log.info(f"#{ctx.channel.name} @{self.nick}: {response}")

    async def event_message(self, message):
        if message.echo:
            return
        if self.channels[message.channel.name]["status"]:
            for listen in self.listeners:
                if await listen(self, message):
                    return
        await self.handle_commands(message)
