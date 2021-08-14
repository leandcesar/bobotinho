# -*- coding: utf-8 -*-
from tortoise import signals

from bobotinho.database.base import Base, ContentMixin, TimestampMixin, fields
from bobotinho.webhook import Webhook


class Bug(Base, TimestampMixin, ContentMixin):
    name = fields.CharField(max_length=64, description="Twitch username")
    channel = fields.CharField(max_length=64, description="Twitch username")

    class Meta:
        table = "bug"


@signals.post_save(Bug)
async def new_bug(sender, instance, created, using_db, update_fields):
    await Webhook.bugs(
        id=instance.id,
        content=instance.content,
        author=instance.name,
        channel=instance.channel,
        timestamp=instance.updated_at,
    )
