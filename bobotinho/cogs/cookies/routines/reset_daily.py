# -*- coding: utf-8 -*-
import os
from datetime import datetime

from bobotinho.database.models import Cookie, User

now = datetime.utcnow()
time = now.replace(hour=6, minute=0, second=0)
if time < now:
    time = time + datetime.timedelta(days=1)


async def routine(bot) -> None:
    os.environ["RESETTING_DAILY"] = "1"
    sponsors = await User.filter(sponsor=True).all().values_list("id", flat=True)
    await Cookie.filter(id__in=sponsors).update(daily=2)
    await Cookie.filter(id__not_in=sponsors).update(daily=1)
    os.environ["RESETTING_DAILY"] = "0"
