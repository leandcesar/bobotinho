# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Optional
from datetime import datetime, timedelta

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
    main_class = UnicodeAttribute(null=False)
    sub_class = UnicodeAttribute(null=False, default=str)
    wins = NumberAttribute(default=0)
    defeats = NumberAttribute(default=0)
    level = NumberAttribute(default=1)
    experience = NumberAttribute(default=0)

    @property
    def total(self) -> float:
        return self.wins + self.defeats

    @property
    def _class(self) -> str:
        if self.main_class and self.sub_class:
            return f"{self.main_class}{self.sub_class}"
        if self.main_class:
            return f"{self.main_class}1"
        return None


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
    user_id = UnicodeAttribute(null=False)
    message = UnicodeAttribute(null=False, default=str)


class Status(MapAttribute, DateTimeMixin):
    online = BooleanAttribute(null=False, default=True, attr_name="on")
    alias = UnicodeAttribute(null=False, default=str)
    message = UnicodeAttribute(null=False, default=str)

    @property
    def offline(self) -> bool:
        return not self.online


class Wedding(MapAttribute, DateTimeMixin):
    user_id = UnicodeAttribute(null=False)
    divorced = BooleanAttribute(null=False, default=False)


class Settings(MapAttribute):
    badge = UnicodeAttribute(null=True)
    block = BooleanAttribute(null=True)
    city = UnicodeAttribute(null=True)
    colors = ListAttribute(null=True, of=UnicodeAttribute, default=list)
    unmention = BooleanAttribute(null=True)
    premium = NumberAttribute(null=True)

    @property
    def mention(self) -> bool:
        return not getattr(self, "unmention", False)


class UserModel(Model, DateTimeMixin):
    class Meta:
        table_name = "user" if config.stage == "prod" else "user-dev"
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

    pets = ListAttribute(null=False, of=Pet, default=list)
    reminders = ListAttribute(null=False, of=Reminder, default=list)
    weddings = ListAttribute(null=False, of=Wedding, default=list)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"

    def __str__(self) -> str:
        return f"@{self.name}"

    @property
    def single(self) -> bool:
        if not self.weddings:
            return True
        return all([wedding.divorced for wedding in self.weddings])

    @classmethod
    def create(cls, id: str, **attrs) -> UserModel:
        instance = cls(str(id), **attrs)
        instance.save()
        return instance

    @classmethod
    def get_or_raise(cls, id: str, **attrs) -> UserModel:
        return cls.get(str(id))

    @classmethod
    def get_or_none(cls, id: str, **attrs) -> Optional[UserModel]:
        try:
            return cls.get(str(id))
        except DoesNotExist:
            return None

    @classmethod
    def get_or_create(cls, id: str, **attrs) -> UserModel:
        return cls.get_or_none(str(id)) or cls.create(id, **attrs)

    @classmethod
    def update_or_none(cls, id: str, **attrs) -> Optional[UserModel]:
        try:
            instance = cls.get(str(id))
            instance.update_user(**attrs)
            return instance
        except DoesNotExist:
            return None

    @classmethod
    def update_or_create(cls, id: str, **attrs) -> UserModel:
        try:
            instance = cls.get(str(id))
            instance.update_user(**attrs)
            return instance
        except DoesNotExist:
            return cls.create(str(id), **attrs)

    def update_user(self, **attrs) -> bool:
        for attr, value in attrs.items():
            setattr(self, attr, value)
        self.updated_on = datetime.utcnow()
        self.save()
        return True

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

    def update_cookie(self, *, daily: bool = False, eat: int = 0, receive: int = 0, donate: int = 0, earnings: int = 0, consume: int = 0) -> bool:
        if not self.cookies:
            self.cookies = Cookies()
        if daily:
            today = datetime.utcnow()
            yesterday = today - timedelta(days=1)
            if self.cookies.daily <= 0 and today.date() == self.cookies.updated_on.date():
                return False
            self.cookies.daily -= 1
            self.cookies.stocked += 1
            if self.cookies.updated_on.date() == yesterday.date():
                self.cookies.streak += 1
            else:
                self.cookies.streak = 0
            self.cookies.updated_on = datetime.utcnow()
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
        elif consume:
            self.cookies.stocked -= consume
        self.save()
        return True

    def update_dungeon(self, *, main_class: str = None, win: bool = False, defeat: bool = False, experience: int = 0, level_up: bool = False) -> bool:
        if not self.dungeons and main_class:
            self.dungeons = Dungeons(main_class=main_class[:2])
        elif self.dungeons and main_class and not win and not defeat and not experience:
            self.dungeons.main_class = main_class[:2]
            self.dungeons.sub_class = main_class[2]
        elif self.dungeons and not main_class and win and not defeat and experience:
            self.dungeons.wins += 1
            self.dungeons.experience += experience
            self.dungeons.level += int(level_up)
            self.dungeons.updated_on = datetime.utcnow()
        elif self.dungeons and not main_class and not win and defeat and not experience:
            self.dungeons.defeats += 1
            self.dungeons.updated_on = datetime.utcnow()
        else:
            raise Exception(f"id={self.id} main_class={main_class} win={win} defeat={defeat} level_up={level_up} experience={experience}")
        self.save()
        return True

    def update_settings(self, *, badge: str = None, city: str = None, color: str = None, mention: bool = None) -> bool:
        if not self.settings:
            self.settings = Settings()
        if badge:
            self.settings.badge = badge
        elif city:
            self.settings.city = city
        elif color:
            if self.settings.colors and len(self.settings.colors) >= 10:
                return False
            elif self.settings.colors:
                self.settings.colors.append(color)
            else:
                self.settings.colors = [color]
        elif mention is not None:
            self.settings.unmention = not mention
        self.save()
        return True

    def add_reminder(self, *, user_id: str, message: str) -> bool:
        if not self.reminders:
            self.reminders = []
        self.reminders.append(Reminder(user_id=str(user_id), message=message))
        self.save()
        return True

    def remove_reminder(self) -> bool:
        self.reminders = self.reminders[1:]
        self.save()
        return True

    def add_pet(self, *, specie: str) -> bool:
        if not self.pets:
            self.pets = []
        self.pets.append(Pet(specie=specie))
        self.save()
        return True

    def remove_pet(self, pet: Pet) -> bool:
        self.pets.remove(pet)
        self.save()
        return True

    def update_pet(self, pet: Pet, *, name: str) -> bool:
        if pet not in self.pets:
            raise Exception(f"id={self.id} pet={pet} name={name}")
        index = self.pets.index(pet)
        pet.name = name
        self.pets[index] = pet
        self.save()
        return True

    def marry(self, *, user_id: str) -> bool:
        if not self.weddings:
            self.weddings = []
        self.weddings.append(Wedding(user_id=str(user_id)))
        self.save()
        return True

    def divorce(self, *, user_id: str) -> bool:
        if not self.weddings:
            return False
        for wedding in self.weddings:
            if wedding.user_id == str(user_id):
                self.weddings.remove(wedding)
                self.save()
                return True
        else:
            return False
