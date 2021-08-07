# -*- coding: utf-8 -*-
import inspect
import os
from importlib import import_module, types
from typing import Optional

from twitchio.ext.commands import (
    Bot,
    Bucket,
    Command,
    Context,
    Cooldown,
)
from twitchio.ext.commands.errors import (
    CheckFailure,
    CommandNotFound,
    CommandOnCooldown,
    MissingRequiredArgument,
)
from twitchio.ext.routines import Routine
from twitchio.message import Message

from bobotinho import log
from bobotinho.apis import AI, Analytics
from bobotinho.database.models import Channel, User
from bobotinho.exceptions import (
    BotIsOffline,
    CommandIsDisabled,
    ContentHasBanword,
    InvalidName,
    UserIsNotAllowed,
)
from bobotinho.utils import checks

DEFAULT_COOLDOWN_RATE = 2
DEFAULT_COOLDOWN_PER = 10
DEFAULT_COOLDOWN_BUCKET = Bucket.user


class Ctx(Context):
    def __init__(self, message: Message, bot: Bot, **kwargs) -> None:
        super().__init__(message, bot, **kwargs)
        self.response: Optional[str] = None
        self.prediction: dict = {}
        self.user: User = None

    def __iter__(self):
        yield "author", getattr(self.author, "id", None)
        yield "channel", getattr(self.channel, "id", None)
        yield "user", getattr(self.user, "id", None)
        yield "message", getattr(self.message, "content", None)
        yield "response", self.response


class TwitchBot(Bot):
    def __init__(self, config):
        super().__init__(
            token=config.access_token,
            client_secret=config.client_secret,
            prefix=config.prefix,
            case_insensitive=True,
        )
        self.mentions: bool = config.ai_url and config.ai_key
        self.owner: str = config.owner
        self.site: str = config.site_url
        self.blocked: list = []
        self.listeners: list = []
        self.routines: list = []
        self.channels: dict = {}
        self.cache: object = None

    async def connect(self) -> None:
        await self._connection._connect()
        for routine in self.routines:
            routine.start(self)

    async def close(self) -> None:
        for routine in self.routines:
            routine.stop()
        await self._connection._close()

    def add_checks(self) -> None:
        for check in [checks.online, checks.enabled, checks.banword]:
            self.check(check)

    def load_commands(self, path: str) -> None:
        for filename in os.listdir(path):
            if not filename.endswith(".py") or filename.startswith("__"):
                continue
            try:
                local: str = os.path.join(path, filename)
                name: str = local[:-3].replace("/", ".")
                package: str = path.replace("/", ".")
                module: types.ModuleType = import_module(name, package=package)
                cooldown: dict = getattr(module, "cooldown", {})
                module.command.__cooldowns__: list = [
                    Cooldown(
                        cooldown.get("rate", DEFAULT_COOLDOWN_RATE),
                        cooldown.get("per", DEFAULT_COOLDOWN_PER),
                        cooldown.get("bucket", DEFAULT_COOLDOWN_BUCKET),
                    )
                ]
                module.command.__checks__: list = getattr(module, "extra_checks", [])
                command: Command = Command(
                    name=getattr(module, "name", filename[:-3]),
                    func=module.command,
                    aliases=getattr(module, "aliases", None),
                    no_global_checks=getattr(module, "no_global_checks", False),
                )
                command.description: str = module.description
                command.usage: Optional[str] = getattr(module, "usage", None)
                self.add_command(command)
            except Exception as e:
                log.error(f"Command '{name}' failed to load: {e}")

    def load_listeners(self, path: str) -> None:
        for filename in os.listdir(path):
            if not filename.endswith(".py") or filename.startswith("__"):
                continue
            try:
                local: str = os.path.join(path, filename)
                name: str = local[:-3].replace("/", ".")
                package: str = path.replace("/", ".")
                module: types.ModuleType = import_module(name, package=package)
                self.listeners.append(module.listener)
            except Exception as e:
                log.error(f"Listener '{name}' failed to load: {e}")

    def load_routines(self, path: str) -> None:
        for filename in os.listdir(path):
            if not filename.endswith(".py") or filename.startswith("__"):
                continue
            try:
                local: str = os.path.join(path, filename)
                name: str = local[:-3].replace("/", ".")
                package: str = path.replace("/", ".")
                module: types.ModuleType = import_module(name, package=package)
                routine: Routine = Routine(
                    coro=module.routine,
                    time=getattr(module, "time", None),
                    delta=getattr(module, "delta", None),
                )
                self.routines.append(routine)
            except Exception as e:
                log.error(f"Routine '{name}' failed to load: {e}")

    def load_cogs(self, base: str = "bobotinho/cogs") -> None:
        self.add_checks()
        for cog in os.listdir(base):
            paths: str = os.listdir(os.path.join(base, cog))
            if "commands" in paths:
                self.load_commands(os.path.join(base, cog, "commands"))
            if "listeners" in paths:
                self.load_listeners(os.path.join(base, cog, "listeners"))
            if "routines" in paths:
                self.load_routines(os.path.join(base, cog, "routines"))

    async def join_all_channels(self) -> None:
        self.channels = {
            channel.user.name: {
                "id": channel.user_id,
                "banwords": list(channel.banwords.keys()),
                "disabled": list(channel.disabled.keys()),
                "online": channel.online,
            } for channel in await Channel.all().select_related("user")
        } or {self.owner.lower(): {"id": 0, "banwords": [], "disabled": [], "online": True}}
        await self.join_channels(list(self.channels))

    async def fetch_blocked(self) -> None:
        self.blocked = await User.filter(block=True).all().values_list("id", flat=True)

    async def reply(self, ctx: Ctx) -> bool:
        if not ctx.response:
            return False
        try:
            response = f"{ctx.user or ctx.author.name}, {ctx.response}"
            await ctx.send(response)
        except Exception as e:
            log.error(e, extra={"ctx": dict(ctx)})
        else:
            log.info(f"#{ctx.channel.name} @{self.nick}: {response}")
            await Analytics.sent(
                self.loop,
                id=ctx.author.id,
                text=response,
                name=ctx.author.name,
                channel=ctx.channel.name,
                intent=ctx.prediction.get("intent"),
                confidence=ctx.prediction.get("confidence"),
            )
            return True
        return False

    async def handle_commands(self, ctx: Ctx) -> bool:
        if ctx.response:
            return False
        if not ctx.prefix:
            return False
        if not ctx.is_valid:
            return False
        if not ctx.prediction:
            log.info(f"#{ctx.channel.name} @{ctx.author.name}: {ctx.message.content}")
            await Analytics.received(
                self.loop,
                id=ctx.author.id,
                text=ctx.message.content,
                name=ctx.author.name,
                channel=ctx.channel.name,
            )
        if not ctx.user:
            ctx.user, _ = await User.get_or_create(
                id=ctx.author.id,
                defaults={
                    "channel": ctx.channel.name,
                    "name": ctx.author.name,
                    "color": ctx.author.colour,
                    "content": ctx.message.content.replace("ACTION", "", 1),
                },
            )
        try:
            await self.invoke(ctx)
        except MissingRequiredArgument:
            ctx.response = ctx.command.usage
        except Exception as e:
            log.error(e, extra={"ctx": dict(ctx)})
        return await self.reply(ctx)

    async def handle_mentions(self, ctx: Ctx) -> bool:
        if ctx.response:
            return False
        if not self.mentions:
            return False
        if not ctx.message.content.startswith((self.nick, f"@{self.nick}")):
            return False
        log.info(f"#{ctx.channel.name} @{ctx.author.name}: {ctx.message.content}")
        await Analytics.received(
            self.loop,
            id=ctx.author.id,
            text=ctx.message.content,
            name=ctx.author.name,
            channel=ctx.channel.name,
        )
        content: str = ctx.message.content.partition(" ")[2]
        prediction: dict = await AI.predict(content)
        intent: str = prediction["intent"]
        entity: str = prediction["entity"]
        confidence: float = prediction["confidence"]
        if intent and confidence > 0.75:
            ctx.message.content: str = f"{self._prefix}{intent} {entity}".strip()
            ctx.response = AI.small_talk(intent)
            return await self.handle_commands(ctx)
        ctx.response = 'não entendi isso, mas tente ver meus comandos digitando "%help"'
        return await self.reply(ctx)

    async def handle_listeners(self, ctx: Ctx) -> bool:
        for listener in self.listeners:
            if ctx.response:
                break
            if inspect.iscoroutinefunction(listener):
                await listener(ctx)
            else:
                listener(ctx)
        return await self.reply(ctx)

    async def event_ready(self) -> None:
        log.info(f"{self.nick} | #{len(self.channels)} | {self._prefix}{len(self.commands)}")

    async def event_command_error(self, ctx: Ctx, e: Exception) -> None:
        if isinstance(e, CommandIsDisabled):
            ctx.response = "esse comando está desativado nesse canal"
        elif isinstance(e, ContentHasBanword):
            ctx.response = "sua mensagem contém um termo banido"
        elif isinstance(e, UserIsNotAllowed):
            ctx.response = "apenas inscritos, VIPs e MODs podem enviar links"
        elif isinstance(e, InvalidName):
            ctx.response = "nome de usuário inválido"
        elif isinstance(e, (BotIsOffline, CommandOnCooldown, CommandNotFound, CheckFailure)):
            log.info(e)
        else:
            ctx.response = "ocorreu um erro inesperado"
            log.error(e, extra={"ctx": dict(ctx)})
        await self.reply(ctx)

    async def event_message(self, message: Message) -> None:
        if message.echo:
            return
        if message.author.id in self.blocked:
            return
        ctx: Ctx = await self.get_context(message, cls=Ctx)
        if self.channels[ctx.channel.name]["online"]:
            ctx.user = await User.update_or_none(ctx)
            await self.handle_listeners(ctx)
            await self.handle_mentions(ctx)
        await self.handle_commands(ctx)
