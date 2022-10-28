# -*- coding: utf-8 -*-
from twitchio.ext.commands.errors import (
    TwitchCommandError,
    InvalidCogMethod,
    InvalidCog,
    MissingRequiredArgument,
    BadArgument,
    ArgumentParsingFailed,
    CommandNotFound,
    CommandOnCooldown,
    CheckFailure,
)

InvalidArgument = (ArgumentParsingFailed, BadArgument, MissingRequiredArgument)
