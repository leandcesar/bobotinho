# -*- coding: utf-8 -*-

from ext import pyramid
from twitchio import Context, Message
from unidecode import unidecode


class Channel:
    def __init__(self, **attrs):
        self.pyramid = pyramid.Pyramid()
        self._status = attrs.get("status", True)
        self._banwords = attrs.get("banwords", [])
        self._disabled = attrs.get("disabled", [])

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if not isinstance(value, bool):
            raise TypeError(f"Expected `bool`, not `{type(value).__name__}`")
        self._status = value

    @property
    def banwords(self):
        return self._banwords

    @banwords.setter
    def banwords(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f"Expected `str`, not `{type(value).__name__}`")
        elif value[0] == "+":
            self._disabled.append(unidecode(value[1:]).lower())
        elif value[0] == "-":
            self._disabled.remove(unidecode(value[1:]).lower())
        else:
            raise ValueError(f"Expected `+` or `-` in `value[0]`, not `{value[0]}`")

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f"Expected `str`, not `{type(value).__name__}`")
        elif value[0] == "+":
            self._disabled.append(value[1:])
        elif value[0] == "-":
            self._disabled.remove(value[1:])
        else:
            raise ValueError(f"Expected `+` or `-` in `value[0]`, not `{value[0]}`")


class Channels(dict):
    def __init__(self, channels: list):
        super().__init__(
            [(channel["name"], Channel(**channel)) for channel in channels]
        )

    def is_banword(self, channel: str, content: str):
        if not isinstance(channel, str):
            raise TypeError(f"Expected `str`, not `{type(channel).__name__}`")
        if not isinstance(content, str):
            raise TypeError(f"Expected `str`, not `{type(content).__name__}`")
        content = unidecode(content).lower()
        return any(banword in content for banword in self[channel].banwords)

    def is_not_banword(self, ctx: Context):
        if not isinstance(ctx, Context):
            raise TypeError(f"Expected `Context`, not `{type(ctx).__name__}`")
        channel = ctx.channel.name
        content = ctx.response if hasattr(ctx, "response") else ctx.content
        return not self.is_banword(channel, content)

    def is_disabled(self, channel: str, command: str):
        if not isinstance(channel, str):
            raise TypeError(f"Expected `str`, not `{type(channel).__name__}`")
        if not isinstance(command, str):
            raise TypeError(f"Expected `str`, not `{type(command).__name__}`")
        return command in self[channel].disabled

    def is_enabled(self, ctx: Context):
        if not isinstance(ctx, Context):
            raise TypeError(f"Expected `Context`, not `{type(ctx).__name__}`")
        channel = ctx.channel.name
        command = ctx.command.name
        return not self.is_disabled(channel, command)

    def is_start_command(self, content: str, prefix: str = "%", start_command: str = "start"):
        if not isinstance(content, str):
            raise TypeError(f"Expected `str`, not `{type(content).__name__}`")
        return content.lower().startswith(prefix + start_command)

    def is_online(self, channel: str):
        if not isinstance(channel, str):
            raise TypeError(f"Expected `str`, not `{type(channel).__name__}`")
        return self[channel].status
    
    def is_offline(self, message: Message):
        if not isinstance(message, Message):
            raise TypeError(f"Expected `Message`, not `{type(message).__name__}`")
        channel = message.channel.name
        content = message.content
        return not self.is_online(channel) and not self.is_start_command(content)
