# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Optional
from datetime import datetime

from pynamodb.attributes import (
    BooleanAttribute,
    ListAttribute,
    MapAttribute,
    NumberAttribute,
    UnicodeAttribute,
    UTCDateTimeAttribute,
)
from pynamodb.exceptions import DoesNotExist
from pynamodb.models import Condition, Model

from bobotinho import config
from bobotinho.models.mixins import DateTimeMixin


class Cookies(MapAttribute, DateTimeMixin):
    daily = NumberAttribute(default=1)
    stocked = NumberAttribute(default=0)
    streak = NumberAttribute(default=0)
    count = NumberAttribute(default=0)
    donated = NumberAttribute(default=0)
    received = NumberAttribute(default=0)


class Dungeons(MapAttribute, DateTimeMixin):
    dungeon = UnicodeAttribute(null=True)
    gender = UnicodeAttribute(null=False)
    main_class = UnicodeAttribute(null=False)
    sub_class = UnicodeAttribute(null=False, default=str)
    wins = NumberAttribute(default=0)
    defeats = NumberAttribute(default=0)
    level = NumberAttribute(default=1)
    experience = NumberAttribute(default=0)

    @property
    def total(self) -> float:
        return self.wins + self.defeats


class Pet(MapAttribute, DateTimeMixin):
    name = UnicodeAttribute(null=False, default=str)
    specie = UnicodeAttribute(null=False)
    # level = NumberAttribute(default=1)
    # experience = NumberAttribute(null=True)
    # energy = NumberAttribute(null=True)
    # fun = NumberAttribute(null=True)
    # hunger = NumberAttribute(null=True)
    # hygiene = NumberAttribute(null=True)
    # love = NumberAttribute(null=True)

    def __str__(self) -> str:
        return self.name if self.name else self.specie


class Reminder(MapAttribute, DateTimeMixin):
    user_id = NumberAttribute(null=False)
    message = UnicodeAttribute(null=False, default=str)
    scheduled_to = UTCDateTimeAttribute(null=True)


class Status(MapAttribute, DateTimeMixin):
    online = BooleanAttribute(null=False, default=True, attr_name="on")
    alias = UnicodeAttribute(null=False, default=str)
    message = UnicodeAttribute(null=False, default=str)


class Wedding(MapAttribute, DateTimeMixin):
    user_id = NumberAttribute(null=False)
    divorced = BooleanAttribute(null=False, default=False)


class Settings(MapAttribute):
    badge = UnicodeAttribute(null=True)
    block = BooleanAttribute(null=True)
    city = UnicodeAttribute(null=True)
    premium = NumberAttribute(null=True)
    colors = ListAttribute(null=True, of=UnicodeAttribute, default=list)


class UserModel(Model, DateTimeMixin):
    class Meta:
        table_name = "user"
        aws_access_key_id = config.aws_access_key_id
        aws_secret_access_key = config.aws_secret_access_key
        region = config.aws_region_name
        read_capacity_units = 5
        write_capacity_units = 5

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute(null=False)
    last_message = UnicodeAttribute(null=False, default=str)
    last_channel = UnicodeAttribute(null=False, default=str)
    last_color = UnicodeAttribute(null=False, default=str)

    cookies = Cookies(null=True)
    dungeons = Dungeons(null=True)
    settings = Settings(null=True)
    status = Status(null=True)

    pets = ListAttribute(null=True, of=Pet)
    reminders = ListAttribute(null=True, of=Reminder)
    weddings = ListAttribute(null=True, of=Wedding)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"

    def __str__(self) -> str:
        return f"@{self.name}"

    @classmethod
    def all(cls, where: Condition = None, limit: int = 100) -> list[UserModel]:
        return [instance for instance in cls.scan(where, limit=limit)]

    @classmethod
    def one(cls, where: Condition = None) -> Optional[UserModel]:
        instances = cls.all(where, limit=1)
        return instances[0] if instances else None

    @classmethod
    def set(cls, pk: int, rk: str = None, **attrs) -> UserModel:
        instance = cls.get(pk, rk)
        for attr, value in attrs.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @classmethod
    def new(cls, pk: int, rk: str = None, **attrs) -> UserModel:
        instance = cls(pk, rk, **attrs)
        instance.save()
        return instance

    @classmethod
    def get_or_new(cls, pk: int, rk: str = None, **attrs) -> UserModel:
        try:
            return cls.get(pk, rk)
        except DoesNotExist:
            return cls.new(pk, **attrs)

    @classmethod
    def get_or_none(cls, pk: int, rk: str = None, **attrs) -> Optional[UserModel]:
        try:
            return cls.get(pk, rk)
        except DoesNotExist:
            return None

    @classmethod
    def set_or_new(cls, pk: int, rk: str = None, **attrs) -> UserModel:
        try:
            return cls.set(pk, rk, **attrs)
        except DoesNotExist:
            return cls.new(pk, rk, **attrs)

    @classmethod
    def set_or_none(cls, pk: int, rk: str = None, **attrs) -> Optional[UserModel]:
        try:
            return cls.set(pk, rk, **attrs)
        except DoesNotExist:
            return None

    def update_status(self, *, online: bool, alias: str = "", message: str = "") -> bool:
        if online and not self.status:
            return True
        if online:
            self.status = None
        if not online and not self.status:
            self.status = Status()
        if not online:
            self.status.online = online
            self.status.alias = alias
            self.status.message = message
        self.save()
        return True

    def update_cookie(self, *, daily: bool = False, eat: int = 0, receive: int = 0, donate: int = 0, earnings: int = 0) -> bool:
        if not self.cookies:
            self.cookies = Cookies()
        if daily:
            if self.cookies.daily <= 0:
                return False
            self.cookies.daily -= 1
            self.cookies.streak += 1
            self.cookies.stocked += 1
        if eat:
            if self.cookies.stocked < eat:
                return False
            self.cookies.stocked -= eat
            self.cookies.count += eat
        elif receive:
            self.cookies.stocked += receive
            self.cookies.received += receive
        elif donate:
            if self.cookies.stocked < donate:
                return False
            self.cookies.stocked -= donate
            self.cookies.donated += donate
        elif earnings:
            self.cookies.stocked += earnings
        self.save()
        return True
