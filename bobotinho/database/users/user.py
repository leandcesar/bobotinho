# -*- coding: utf-8 -*-
from bobotinho.database.base import Base, ContentMixin, TimestampMixin, UserMixin, fields


class User(Base, UserMixin, TimestampMixin, ContentMixin):
    color = fields.CharField(max_length=7, null=True, description="Twitch color")
    channel = fields.CharField(max_length=64, null=True, description="Twitch channel")
    saved_color = fields.CharField(max_length=7, null=True)
    city = fields.CharField(max_length=100, null=True)

    class Meta:
        app = "users"
        table = "user"

    def __str__(self):
        return self.name

    @classmethod
    async def create_if_not_exists(cls, ctx):
        if not await cls.exists(id=ctx.author.id):
            await cls.create(
                id=ctx.author.id,
                channel=ctx.channel.name,
                name=ctx.author.name,
                color=ctx.author.colour,
                content=ctx.content,
            )

    @classmethod
    async def update_if_exists(cls, message):
        if instance := await cls.get_or_none(id=message.author.id):
            attrs = ["name", "channel", "color", "content"]
            values = [message.author.name, message.channel.name, message.author.colour, message.content]
            update_fields = []
            for attr, value in zip(attrs, values):
                if attr == "content" and len(value) > 500:
                    value = value[:500]
                if getattr(instance, attr) != value:
                    setattr(instance, attr, value)
                    update_fields.append(attr)
            if update_fields:
                update_fields.append("updated_at")
                await instance.save(update_fields=update_fields)
