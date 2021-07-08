# -*- coding: utf-8 -*-
from bobotinho.autobot import (  # NOQA
    CheckFailure,
    CommandNotFound,
    MissingRequiredArgument,
)
from bobotinho.utils.checks import (  # NOQA
    BotIsNotOnline,
    ContentHasBanword,
    CommandIsDisabled,
    CommandIsOnCooldown,
    UserIsNotAllowed,
    UserIsNotASponsor,
)
