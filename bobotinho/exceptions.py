# -*- coding: utf-8 -*-


class BobotinhoException(Exception):
    pass


class CheckException(BobotinhoException):
    pass


class RequestException(BobotinhoException):
    pass


class BotIsOffline(CheckException):
    def __init__(self, *, channel: str) -> None:
        super().__init__(f"Bot is offline on '{channel}' channel.")


class ContentHasBanword(CheckException):
    def __init__(self, *, channel: str, content: str) -> None:
        super().__init__(f"'{content}' content has a banword on '{channel}' channel.")


class CommandIsDisabled(CheckException):
    def __init__(self, *, channel: str, command: str) -> None:
        super().__init__(f"'{command}' command is disabled on '{channel}' channel.")


class UserIsNotAllowed(CheckException):
    def __init__(self, *, channel: str, user: str) -> None:
        super().__init__(f"'{user}' user is not allowed to send links on '{channel}' channel.")


class InvalidName(BobotinhoException):
    pass


class WebhookUrlNotDefined(RequestException):
    def __init__(self) -> None:
        super().__init__("<BOT_WEBHOOK_URL> not defined, webhook not sent.")
