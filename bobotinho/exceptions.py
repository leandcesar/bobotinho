# -*- coding: utf-8 -*-

class BobotinhoException(Exception):
    pass


class CheckException(BobotinhoException):
    pass


class RequestException(BobotinhoException):
    pass


class BotIsOffline(CheckException):
    pass


class ContentHasBanword(CheckException):
    pass


class CommandIsDisabled(CheckException):
    pass


class UserIsNotAllowed(CheckException):
    pass


class GameIsAlreadyRunning(CheckException):
    pass


class InvalidName(BobotinhoException):
    pass
