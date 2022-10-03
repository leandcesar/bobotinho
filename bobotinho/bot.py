# -*- coding: utf-8 -*-
from bobotinho import config, logger
from bobotinho.ext.cache import cache
from bobotinho.ext.commands import (
    Any,
    Bot,
    Callable,
    Context,
    Coroutine,
    Message,
    routine,
)
from bobotinho.ext.exceptions import (
    CheckFailure,
    CommandNotFound,
    CommandOnCooldown,
    InvalidArgument,
)
from bobotinho.models.channel import ChannelModel
from bobotinho.models.user import UserModel
from bobotinho.services.dashbot import Dashbot


class Bobotinho(Bot):
    listeners: list[Callable[[Context,], Coroutine[Any, Any, bool]]] = []
    channels: dict[str, ChannelModel] = {}
    dashbot: Dashbot

    def load_modules(self, cogs: list[str]) -> None:
        for cog in cogs:
            module = cog.replace("/", ".")
            self.load_module(module)

    def is_online(self, message: Message) -> bool:
        return self.channels[message.channel.name].online is True

    def is_enabled(self, ctx: Context, command: str = "") -> bool:
        command_name = command or ctx.command.name
        return command_name.lower() not in self.channels[ctx.channel.name].commands_disabled

    async def before_connect(self) -> None:
        self.check(self.is_enabled)
        self.dashbot = Dashbot(key=config.dashbot_key)

    async def after_connect(self) -> None:
        self.new_channels.start()
        self.check_channels.start()

    async def before_close(self) -> None:
        self.new_channels.cancel()
        self.check_channels.cancel()

    async def after_close(self) -> None:
        await self.dashbot.close()

    def start(self) -> None:
        self.loop.run_until_complete(self.before_connect())
        self.loop.create_task(self.connect())
        self.loop.run_until_complete(self.after_connect())
        self.loop.run_forever()

    def stop(self) -> None:
        self.loop.run_until_complete(self.before_close())
        self.loop.run_until_complete(self.close())
        self.loop.run_until_complete(self.after_close())
        self.loop.close()

    async def event_ready(self) -> None:
        ...

    async def global_before_invoke(self, ctx: Context) -> None:
        if not ctx.user:
            ctx.user = UserModel.set_or_new(
                ctx.author.id,
                name=ctx.author.name,
                last_message=ctx.message.content,
                last_channel=ctx.channel.name,
                last_color=ctx.author.color,
            )

    async def global_after_invoke(self, ctx: Context) -> None:
        # TODO
        # await self.dashbot.received(id=ctx.author.id, name=ctx.author.name, message=ctx.message.content, locale=ctx.channel.name)
        ...

    async def event_message(self, message: Message) -> None:
        if message.echo:
            # TODO
            # await self.dashbot.received(id=message.author.id, name=message.author.name, message=message.content, locale=message.channel.name)
            return None
        if not self.is_online(message):
            return None
        ctx = await self.get_context(message, cls=Context)
        # TODO
        # ctx.user = UserModel.set_or_none(
        #     ctx.author.id,
        #     name=ctx.author.name,
        #     last_message=ctx.message.content,
        #     last_channel=ctx.channel.name,
        #     last_color=ctx.author.color,
        # )
        for listener in self.listeners:
            if await listener(ctx):
                return None
        try:
            await self.invoke(ctx)
        except InvalidArgument:
            if ctx.command and hasattr(ctx.command, "usage"):
                return await ctx.reply(ctx.command.usage)
            return await ctx.reply("ocorreu um erro inesperado")
        except Exception as error:
            logger.error(error, extra={"ctx": dict(ctx)}, exc_info=error)

    async def event_error(self, error: Exception, data: str = None) -> None:
        logger.error(error, exc_info=error)

    async def event_command_error(self, ctx: Context, error: Exception) -> None:
        if isinstance(error, CommandNotFound):
            return None
        if isinstance(error, CheckFailure):
            return None
        if isinstance(error, CommandOnCooldown):
            return None
        if isinstance(error, NotImplementedError):
            return await ctx.reply("temporariamente desativado")
        if isinstance(error, InvalidArgument):
            if ctx.command and hasattr(ctx.command, "usage"):
                return await ctx.reply(ctx.command.usage)
        logger.error(error, extra={"ctx": dict(ctx)}, exc_info=error)
        return await ctx.reply("ocorreu um erro inesperado")

    @routine(seconds=30, wait_first=True)
    async def check_channels(self) -> None:
        connected_channels = [channel.name for channel in self.connected_channels]
        disconnected_channels = [channel for channel in self.channels if channel not in connected_channels]
        await self.join_channels(disconnected_channels)

    @routine(seconds=600)
    async def new_channels(self) -> None:
        channels_id = [channel.id for channel in self.channels.values()]
        condition = ~ChannelModel.id.is_in(*channels_id) if channels_id else None
        for channel in ChannelModel.all(condition):
            self.channels[channel.name] = channel
