# -*- coding: utf-8 -*-
from tortoise import timezone
from tortoise.fields import (
    BooleanField,
    CharField,
    DatetimeField,
    ForeignKeyField,
    IntField,
    JSONField,
    SmallIntField,
)
from tortoise.models import Model, Q


class Base(Model):
    id = IntField(pk=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)

    @classmethod
    async def exists_or(cls, **kwargs):
        return await cls.exists(Q(join_type=Q.OR, **kwargs))


class TimestampMixin:
    created_at = DatetimeField(auto_now_add=True)
    updated_at = DatetimeField(auto_now=True)

    @property
    def created_ago(cls):
        return timezone.now() - cls.created_at

    @property
    def updated_ago(cls):
        return timezone.now() - cls.updated_at


class ContentMixin:
    content = CharField(max_length=500, null=True, description="Twitch message content")


class User(Base, TimestampMixin, ContentMixin):
    id = IntField(pk=True, description="Twitch ID")
    name = CharField(unique=True, index=True, max_length=64, description="Twitch username")
    color = CharField(max_length=7, null=True, description="Twitch color")
    channel = CharField(max_length=64, null=True, description="Twitch channel")
    saved_color = CharField(max_length=7, null=True)

    class Meta:
        table = "user"

    def __str__(self):
        return self.name

    @classmethod
    async def create_if_not_exists(cls, ctx):
        if not await cls.get_or_none(id=ctx.author.id):
            return await cls.create(
                id=ctx.author.id,
                channel=ctx.channel.name,
                name=ctx.author.name,
                color=ctx.author.colour,
                content=ctx.content,
            )

    @classmethod
    async def update_if_exists(cls, message):
        if user := await cls.get_or_none(id=message.author.id):
            return await user.update_from_dict({
                "channel": message.channel.name,
                "name": message.author.name,
                "color": message.author.colour,
                "content": message.content,
            }).save()


class Channel(Base, TimestampMixin):
    user = ForeignKeyField("models.User", to_field="name")
    followers = IntField(null=True, description="Twitch followers")
    icon = CharField(max_length=64, null=True, description="Twitch profile icon")
    banwords = JSONField(default={})
    disabled = JSONField(default={})
    status = BooleanField(default=True)

    class Meta:
        table = "channel"

    def __str__(self):
        return self.user_id

    @classmethod
    async def append_json(cls, name, field, key, value):
        channel = await cls.get(user_id=name)
        json = getattr(channel, field)
        json[key] = value
        setattr(channel, field, json)
        await channel.save()

    @classmethod
    async def remove_json(cls, name, field, key):
        channel = await cls.get(user_id=name)
        json = getattr(channel, field)
        json.pop(key)
        setattr(channel, field, json)
        await channel.save()


class Afk(Base, TimestampMixin, ContentMixin):
    user = ForeignKeyField("models.User", to_field="name")
    alias = CharField(max_length=8, null=True)
    status = BooleanField(default=False)

    class Meta:
        table = "afk"

    @classmethod
    async def update_or_create_from_ctx(cls, ctx, content):
        if afk := await cls.get_or_none(user_id=ctx.author.name):
            return await afk.update_from_dict({
                "alias": ctx.command.invocation,
                "status": True,
                "content": content,
            }).save()
        return await cls.create(
            user_id=ctx.author.name,
            alias=ctx.command.invocation,
            status=True,
            content=ctx.content,
        )


class Cookie(Base):
    user = ForeignKeyField("models.User", to_field="name")
    count = SmallIntField(default=0)
    daily = SmallIntField(default=1)
    donated = SmallIntField(default=0)
    received = SmallIntField(default=0)
    stocked = SmallIntField(default=0)

    class Meta:
        table = "cookie"

    @classmethod
    async def use_daily(cls):
        if not cls.daily:
            return False
        cls.daily -= 1
        await cls.save()
        return True

    @classmethod
    async def consume(cls, amount: int = 1):
        if cls.stocked + cls.daily < amount:
            return False
        if cls.stocked >= amount:
            cls.stocked -= amount
        else:
            amount -= cls.stocked
            cls.stocked = 0
            cls.daily -= amount
        cls.count += amount
        await cls.save()
        return True

    @classmethod
    async def donate(cls, amount: int = 1):
        if cls.daily < amount:
            return False
        cls.daily -= amount
        cls.donated += amount
        await cls.save()
        return True

    @classmethod
    async def receive(cls, amount: int = 1):
        cls.stocked += amount
        cls.received += amount
        await cls.save()
        return True

    @classmethod
    async def stock(cls, amount: int = 1):
        cls.stocked += amount
        await cls.save()
        return True


class Dungeon(Base, TimestampMixin):
    user = ForeignKeyField("models.User", to_field="name")
    class_ = CharField(max_length=1)
    sub_class = CharField(max_length=1, default="A", null=True)
    gender = CharField(max_length=1)
    i = CharField(max_length=3, null=True)
    wins = SmallIntField(default=0)
    defeats = SmallIntField(default=0)
    raid_wins = SmallIntField(default=0)
    raid_defeats = SmallIntField(default=0)
    # boss_wins = SmallIntField(default=0)
    # boss_defeats = SmallIntField(default=0)
    level = IntField(default=1)
    xp = IntField(default=0)
    # gold = IntField(default=0)
    # points = SmallIntField(default=0)
    # strenght = SmallIntField(default=0)
    # intelligence = SmallIntField(default=0)
    # dexterity = SmallIntField(default=0)
    # constitution = SmallIntField(default=0)
    # charisma = SmallIntField(default=0)

    class Meta:
        table = "dungeon"


class Pet(Base):
    user = ForeignKeyField("models.User", to_field="name")
    name = CharField(max_length=32, null=True)
    specie = CharField(max_length=16)
    xp = IntField(default=0)
    energy = SmallIntField(default=10)
    fun = SmallIntField(default=0)
    hunger = SmallIntField(default=0)
    hygiene = SmallIntField(default=0)
    love = SmallIntField(default=0)

    class Meta:
        table = "pet"

    def __str__(self):
        return self.name if self.name else self.specie


class Reminder(Base, TimestampMixin, ContentMixin):
    channel = ForeignKeyField("models.User", to_field="name", related_name="reminders_on")
    user_from = ForeignKeyField("models.User", to_field="name", related_name="reminders_to")
    user_to = ForeignKeyField("models.User", to_field="name", related_name="reminders_from")
    scheduled_for = DatetimeField(null=True)

    class Meta:
        table = "reminder"

    @property
    def scheduled_ago(cls):
        return cls.scheduled_for - timezone.now()


class Suggest(Base, ContentMixin):
    user = ForeignKeyField("models.User", to_field="name")

    class Meta:
        table = "suggest"


class Wedding(Base, TimestampMixin):
    user_1 = ForeignKeyField("models.User", to_field="name", related_name="user_1")
    user_2 = ForeignKeyField("models.User", to_field="name", related_name="user_2")
    divorced = BooleanField(default=False)

    class Meta:
        table = "wedding"
