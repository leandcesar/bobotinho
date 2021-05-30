# -*- coding: utf-8 -*-
from tortoise import signals
from tortoise.exceptions import TransactionManagementError

from bobotinho.webhook import Webhook
from bobotinho.database import models


@signals.post_save(models.SystemLog)
async def update_system_log(sender, instance, created, using_db, update_fields):
    await Webhook.status(instance, created)


@signals.post_save(models.User)
async def update_user_name(sender, instance, created, using_db, update_fields):
    if not created and update_fields and "name" in update_fields:
        try:
            await models.Cookie.filter(id=instance.id).update(name=instance.name)
        except TransactionManagementError:
            if cookie := await models.Cookie.get_or_none(name=instance.name):
                await cookie.delete()
        try:
            await models.Player.filter(id=instance.id).update(name=instance.name)
        except TransactionManagementError:
            if player := await models.Player.get_or_none(name=instance.name):
                await player.delete()


@signals.post_save(models.Suggest)
async def new_suggest(sender, instance, created, using_db, update_fields):
    await Webhook.suggestions(instance)


# @signals.pre_save(Table)
# async def user_pre_save(sender, instance, using_db, update_fields):
#     print(sender, instance, using_db, update_fields)


# @signals.post_save(Table)
# async def user_post_save(sender, instance, created, using_db, update_fields):
#     print(sender, instance, using_db, created, update_fields)


# @signals.pre_delete(Table)
# async def user_pre_delete(sender, instance, using_db):
#     print(sender, instance, using_db)


# @signals.post_delete(Table)
# async def user_post_delete(sender, instance, using_db):
#     print(sender, instance, using_db)
