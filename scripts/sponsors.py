# -*- coding: utf-8 -*-
import root  # NOQA
from tqdm import tqdm
from tortoise.exceptions import DoesNotExist

from bobotinho import db, loop, log
from bobotinho.database import models

NEW_SPONSORS = {}
BOBOTINHO_ID = 488743876
REMIND_CONTENT = (
    "oi, você acaba de receber {cookies} cookies, "
    "triplo de limite de lembretes, acesso ao comando \"%badge\" "
    "e outras vantagens! Obrigado por apoiar 💜"
)


async def get_user_id(name: str) -> int:
    user: models.User = await models.User.get(name=name)
    return user.id


async def set_sponsor(user_id: int) -> None:
    await models.User.filter(id=user_id).update(sponsor=True)


async def set_cookies(name: str, user_id: int, cookies: int) -> None:
    if user := await models.Cookie.get_or_none(id=user_id):
        user.stocked += cookies
        await user.save()
    else:
        await models.Cookie.create(id=user_id, name=name, stocked=cookies)


async def set_remind(user_id: int, cookies: int) -> None:
    content: str = REMIND_CONTENT.format(cookies=cookies)
    await models.Reminder.create(
        from_user_id=BOBOTINHO_ID,
        to_user_id=user_id,
        channel_id=BOBOTINHO_ID,
        content=content,
    )


async def main() -> None:
    new_sponsors: dict = NEW_SPONSORS
    with tqdm(total=len(new_sponsors)) as progress_bar:
        for name, value in new_sponsors.items():
            name: str = name.lower()
            value: int = int(value * 10)
            try:
                user_id: int = await get_user_id(name)
            except DoesNotExist:
                log.warning(f"Sponsor with username @{name} was not found")
                continue
            except Exception as e:
                log.error(f"Exception for sponsor with username @{name}: {e}")
                continue
            else:
                await set_sponsor(user_id)
                await set_cookies(name, user_id, value)
                await set_remind(user_id, value)
            progress_bar.update(1)


if __name__ == "__main__":
    try:
        loop.run_until_complete(db.init())
        loop.run_until_complete(main())
    except BaseException as e:
        print(e)
    finally:
        loop.run_until_complete(db.close())
