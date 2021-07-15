# -*- coding: utf-8 -*-
from bobotinho.apis.ai import AI
from bobotinho.apis.analytics import Analytics
from bobotinho.autobot import AutoBot, Context
from bobotinho.cache import cache
from bobotinho.database import models
from bobotinho.exceptions import (
    BotIsNotOnline,
    CheckFailure,
    CommandIsDisabled,
    CommandIsOnCooldown,
    CommandNotFound,
    ContentHasBanword,
    MissingRequiredArgument,
    UserIsNotAllowed,
    UserIsNotASponsor,
)
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
        self.cache = cache
        self.cooldowns = cache
        self.blocked = []
        if config.ai:
            self.add_listener(self.event_mention, "event_message")

    async def add_all_channels(self):
        self.channels = {
            channel.user.name: {
                "id": channel.user.id,
                "banwords": list(channel.banwords.keys()),
                "disabled": list(channel.disabled.keys()),
                "online": channel.online,
            } for channel in await models.Channel.all().select_related("user")
        }
        await self.join_all_channels(list(self.channels.keys()))

    async def event_ready(self):
        self.add_all_commands()
        self.add_all_listeners()
        self.add_all_tasks()
        self.add_all_checks([checks.online, checks.enabled, checks.cooldown])
        await self.add_all_channels()
        self.blocked = await models.User.filter(block=True).all().values_list("id", flat=True)
        log.info(f"{self.nick} | #{len(self.channels)} | {self.prefixes[0]}{len(self.commands)}")

    async def event_error(self, e, data=None):
        log.exception(e)

    async def event_command_error(self, ctx, e):
        if isinstance(e, CommandIsDisabled):
            ctx.response = "esse comando está desativado nesse canal"
        elif isinstance(e, ContentHasBanword):
            ctx.response = "sua mensagem contém um termo banido"
        elif isinstance(e, UserIsNotAllowed):
            ctx.response = "apenas inscritos, VIPs e MODs podem enviar links"
        elif isinstance(e, UserIsNotASponsor):
            ctx.response = f'apenas apoiadores podem usar esse comando, digite "{ctx.prefix}donate"'
        elif isinstance(e, CheckFailure):
            log.error(e)
        if ctx.response:
            response = f"{ctx.user}, {ctx.response}"
            await ctx.send(response)
            await Analytics.sent(ctx)
        elif isinstance(e, MissingRequiredArgument) and ctx.command.usage:
            ctx.response = ctx.command.usage
        elif not isinstance(e, (BotIsNotOnline, CheckFailure, CommandIsOnCooldown, CommandNotFound)):
            log.exception(e)

    async def get_context(self, message) -> Context:
        prefix = await self.get_prefix(message)
        ctx = Context(
            message=message,
            channel=message.channel,
            user=message.author,
            prefix=prefix,
        )
        ctx.bot = self
        ctx.response = None
        return ctx

    async def global_before_hook(self, ctx):
        await Analytics.received(ctx)
        ctx.command.invocation = ctx.content.partition(" ")[0][len(ctx.prefix):]
        ctx.prefix = self.prefixes[0]
        ctx.user, _ = await models.User.get_or_create(
            id=ctx.author.id,
            defaults={
                "channel": ctx.channel.name,
                "name": ctx.author.name,
                "color": ctx.author.colour,
                "content": ctx.content,
            },
        )

    async def global_after_hook(self, ctx):
        if not ctx.response:
            log.error(f'"{ctx.content}" from @{ctx.author.name} has no ctx.response')
            ctx.response = ctx.command.usage or "ocorreu um erro inesperado"
        elif len(ctx.response) > 500:
            log.error(f'"{ctx.response}" > 500 characters')
            ctx.response = "esse comando gerou uma resposta muito grande"
        ctx.response = f"{ctx.user}, {ctx.response}"
        await ctx.send(ctx.response)
        await Analytics.sent(ctx)

    async def reply_mention(self, message):
        mention, _, content = message.content.partition(" ")
        prediction = await AI.nlu(content)
        intent = prediction["intent"]
        entity = prediction["entity"] or ""
        if response := AI.small_talk(intent):
            response = f"@{message.author.name}, {response}"
            await message.channel.send(response)
        else:
            message.content = f"{self.prefixes[0]}{intent} {entity}".strip()
            await self.handle_commands(message)

    async def event_listener(self, message):
        for listen in self.listeners:
            if await listen(self, message):
                return True

    async def event_message(self, message):
        if message.echo:
            return
        if message.author.id in self.blocked:
            return
        if self.channels[message.channel.name]["online"]:
            await models.User.update_if_exists(message)
            if await self.event_listener(message):
                return
        await self.handle_commands(message)

    async def event_mention(self, message):
        if message.echo:
            return
        if message.author.id in self.blocked:
            return
        if not self.channels[message.channel.name]["online"]:
            return
        if not message.content.startswith((self.nick, f"@{self.nick}")):
            return
        await self.reply_mention(message)
