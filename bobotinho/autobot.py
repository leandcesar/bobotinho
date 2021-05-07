# -*- coding: utf-8 -*-
import inspect
import os
from concurrent.futures._base import TimeoutError
from importlib import import_module
from twitchio.dataclasses import Context
from twitchio.ext.commands import Bot, Command
from twitchio.ext.commands.errors import CheckFailure, CommandNotFound, MissingRequiredArgument  # NOQA

from bobotinho.logger import log


class AutoBot(Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def _handle_checks(self, ctx, no_global_checks=False):
        if no_global_checks:
            _checks = ctx.command._checks
        else:
            _checks = self._checks + ctx.command._checks
        if not _checks:
            return True
        for predicate in _checks:
            if inspect.iscoroutinefunction(predicate):
                result = await predicate(ctx)
            else:
                result = predicate(ctx)
            if not result:
                return predicate
        return True

    async def get_context(self, message):
        prefix = await self.get_prefix(message)
        ctx = Context(
            message=message,
            channel=message.channel,
            user=message.author,
            prefix=prefix,
        )
        ctx.bot = self
        return ctx

    def add_all_commands(self, basedir: str = "bobotinho/cogs/commands"):
        for path in [filename.path for filename in os.scandir(basedir) if filename.is_dir()]:
            if path.endswith("__pycache__"):
                continue
            for filename in os.listdir(path):
                if not filename.endswith(".py") or filename == "__init__.py":
                    continue
                try:
                    local = os.path.join(path, filename)
                    module = import_module(local[:-3].replace("/", "."), basedir.replace("/", "."))
                    module.func._checks = getattr(module, "extra_checks", [])
                    command = Command(
                        name=getattr(module, "name", filename[:-3]),
                        func=module.func,
                        aliases=getattr(module, "aliases", None),
                        no_global_checks=getattr(module, "no_global_checks", False),
                    )
                    command.description = module.description
                    command.usage = getattr(module, "usage", None)
                    self.add_command(command)
                except Exception as e:
                    log.exception(e)

    def add_all_listeners(self, basedir: str = "bobotinho/cogs/listeners"):
        self.listeners = []
        for filename in os.listdir(basedir):
            if not filename.endswith(".py") or filename == "__init__.py":
                continue
            try:
                local = os.path.join(basedir, filename)
                module = import_module(local[:-3].replace("/", "."), basedir.replace("/", "."))
                members = inspect.getmembers(module)
                for name, member in members:
                    if name.startswith('event_'):
                        self.listeners.append(member)
            except Exception as e:
                log.exception(e)

    def add_all_tasks(self, basedir: str = "bobotinho/cogs/tasks"):
        for filename in os.listdir(basedir):
            if not filename.endswith(".py") or filename == "__init__.py":
                continue
            try:
                local = os.path.join(basedir, filename)
                module = import_module(local[:-3].replace("/", "."), basedir.replace("/", "."))
                self.loop.create_task(module.func(self))
            except Exception as e:
                log.exception(e)

    def add_all_checks(self, checks: list = []) -> list:
        failed = []
        for check in checks:
            try:
                self.add_check(check)
            except Exception as e:
                failed.append(check)
                log.exception(e)
        return failed

    async def join_all_channels(self, channels: list = []) -> list:
        failed = []
        for channel in channels:
            try:
                await self.join_channels([channel])
            except TimeoutError as e:
                failed.append(channel)
                log.error(e)
            except Exception as e:
                failed.append(channel)
                log.exception(e)
        return failed