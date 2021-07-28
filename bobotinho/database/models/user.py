# -*- coding: utf-8 -*-
from bobotinho.database.base import Base, ContentMixin, TimestampMixin, UserMixin, fields


class User(Base, UserMixin, TimestampMixin, ContentMixin):
    color = fields.CharField(max_length=7, null=True, description="Twitch color")
    channel = fields.CharField(max_length=64, null=True, description="Twitch channel")
    saved_color = fields.CharField(max_length=7, null=True)
    city = fields.CharField(max_length=100, null=True)
    ping = fields.BooleanField(default=True)
    mention = fields.BooleanField(default=True)
    block = fields.BooleanField(default=False)
    sponsor = fields.BooleanField(default=False)
    badge = fields.CharField(max_length=16, null=True)

    class Meta:
        table = "user"

    def __rep__(self):
        if self.sponsor and self.badge:
            return f"{self.badge} @{self.name}"
        return f"@{self.name}"

    def __str__(self):
        if self.sponsor and self.badge:
            return f"{self.badge} @{self.name}"
        return f"@{self.name}"

    @classmethod
    async def update_if_exists(cls, message):
        if instance := await cls.get_or_none(id=message.author.id):
            attrs = {
                "name": message.author.name,
                "channel": message.channel.name,
                "color": message.author.colour,
                "content": message.content.replace("ACTION", "", 1),
            }
            update_fields = []
            for attr, value in attrs.items():
                if attr == "content" and len(value) > 500:
                    value = value[:500]
                if getattr(instance, attr) != value:
                    setattr(instance, attr, value)
                    update_fields.append(attr)
            if update_fields:
                update_fields.append("updated_at")
                await instance.save(update_fields=update_fields)
