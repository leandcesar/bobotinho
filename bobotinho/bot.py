# -*- coding: utf-8 -*-
from bobotinho.autobot import AutoBot, CheckFailure, CommandNotFound, MissingRequiredArgument
from bobotinho.apis.analytics import Analytics
from bobotinho.apis.ai import AI
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
        self.cooldowns = {}
        self.cache = {}
        if config.ai:
            self.add_listener(self.event_mention, "event_message")

    async def add_all_channels(self):
        self.channels = {
            channel.user.name: {
                "id": channel.user.id,
                "banwords": list(channel.banwords.keys()),
                "disabled": list(channel.disabled.keys()),
                "status": channel.status,
            } for channel in await models.Channel.all().select_related("user")
        }
        await self.join_all_channels(list(self.channels.keys()))

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
        if isinstance(e, CommandNotFound):
            pass
        elif isinstance(e, CheckFailure):
            if str(e).split()[-1] in ["is_online", "is_cooldown"]:
                pass
            elif str(e).split()[-1] == "is_enabled":
                ctx.response = "esse comando está desativado nesse canal"
            elif str(e).split()[-1] == "is_banword":
                ctx.response = "sua mensagem contém um termo banido"
            elif str(e).split()[-1] == "is_allowed":
                ctx.response = "apenas inscritos, VIPs e MODs podem enviar links"
            else:
                log.error(e)
            if hasattr(ctx, "response"):
                response = f"@{ctx.author.name}, {ctx.response}"
                await ctx.send(response)
                log.debug(f"#{ctx.channel.name} @{self.nick}: {response}")
                await Analytics.sent(ctx)
        elif isinstance(e, MissingRequiredArgument) and ctx.command.usage:
            ctx.response = ctx.command.usage
        else:
            log.exception(e)

    async def global_before_hook(self, ctx):
        log.debug(f"#{ctx.channel.name} @{ctx.author.name}: {ctx.content}")
        await Analytics.received(ctx)
        ctx.command.invocation = ctx.content.partition(" ")[0][len(ctx.prefix):]
        ctx.prefix = self.prefixes[0]
        await models.User.create_if_not_exists(ctx)

    async def global_after_hook(self, ctx):
        if not hasattr(ctx, "response"):
            log.error(f'"{ctx.content}" from @{ctx.author.name} has no ctx.response')
            ctx.response = ctx.command.usage or "ocorreu um erro inesperado"
        elif len(ctx.response) > 400:
            log.info(f'"{ctx.response}" > 400 characters')
            ctx.response = "esse comando gerou uma resposta muito grande"
        response = f"@{ctx.author.name}, {ctx.response}"
        await ctx.send(response)
        log.debug(f"#{ctx.channel.name} @{self.nick}: {response}")
        await Analytics.sent(ctx)

    async def event_message(self, message):
        if message.echo:
            return
        await models.User.update_if_exists(message)
        if self.channels[message.channel.name]["status"]:
            for listen in self.listeners:
                if await listen(self, message):
                    return
        await self.handle_commands(message)

    async def event_mention(self, message):
        if message.echo:
            return
        mention, _, content = message.content.partition(" ")
        if mention not in [self.nick, f"@{self.nick}", f"{self.nick},", f"@{self.nick},"]:
            return
        prediction = await AI.nlu(content)
        if AI.is_small_talk(prediction):
            intent = prediction["intent"]
            response = f"@{message.author.name}, {AI.response(intent)}"
            await message.channel.send(response)
            log.debug(f"#{message.channel.name} @{self.nick}: {response}")
        else:
            command = prediction["intent"]
            arg = prediction["entity"] or ""
            message.content = f"{self.prefixes[0]}{command} {arg}".strip()
            await self.handle_commands(message)
