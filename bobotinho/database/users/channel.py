# -*- coding: utf-8 -*-
from bobotinho.database.base import Base, TimestampMixin, fields


class Channel(Base, TimestampMixin):
    user = fields.ForeignKeyField("users.User")
    followers = fields.IntField(null=True, description="Twitch followers")
    banwords = fields.JSONField(default={})
    disabled = fields.JSONField(default={})
    status = fields.BooleanField(default=True)

    class Meta:
        app = "users"
        table = "channel"

    @classmethod
    async def append_json(cls, id, field, key, value):
        instance = await cls.get(user_id=id)
        json = getattr(instance, field)
        json[key] = value
        setattr(instance, field, json)
        await instance.save()

    @classmethod
    async def remove_json(cls, id, field, key):
        instance = await cls.get(user_id=id)
        json = getattr(instance, field)
        json.pop(key)
        setattr(instance, field, json)
        await instance.save()
