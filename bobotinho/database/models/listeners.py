# -*- coding: utf-8 -*-
from tortoise import signals

from bobotinho.webhook import Webhook
from bobotinho.database import models


@signals.post_save(models.User)
async def update_user_name(sender, instance, created, using_db, update_fields):
    if not created and update_fields and "name" in update_fields:
        await models.Cookie.filter(id=instance.id).update(name=instance.name)
        await models.Player.filter(id=instance.id).update(name=instance.name)


@signals.post_save(models.Suggest)
async def new_suggest(sender, instance, created, using_db, update_fields):
    await Webhook.suggestions(instance)
