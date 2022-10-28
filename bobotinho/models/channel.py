# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Optional

from pynamodb.attributes import (
    BooleanAttribute,
    ListAttribute,
    NumberAttribute,
    UnicodeAttribute,
)
from pynamodb.exceptions import DoesNotExist
from pynamodb.models import Condition, Model

from bobotinho import config
from bobotinho.models.mixins import DateTimeMixin


class ChannelModel(Model, DateTimeMixin):
    class Meta:
        table_name = "channel" if config.stage == "prod" else "channel-dev"
        aws_access_key_id = config.aws_access_key_id
        aws_secret_access_key = config.aws_secret_access_key
        region = config.aws_region_name
        read_capacity_units = 5
        write_capacity_units = 5

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute(null=False)
    online = BooleanAttribute(default=True)
    commands_disabled = ListAttribute(of=UnicodeAttribute, default=list)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"

    def __str__(self) -> str:
        return f"@{self.name}"

    @property
    def offline(self) -> bool:
        return not self.online

    @classmethod
    def create(cls, id: str, **attrs) -> ChannelModel:
        instance = cls(str(id), **attrs)
        instance.save()
        return instance

    @classmethod
    def get_or_raise(cls, id: str, **attrs) -> ChannelModel:
        return cls.get(str(id))

    @classmethod
    def get_or_none(cls, id: str, **attrs) -> Optional[ChannelModel]:
        try:
            return cls.get(str(id))
        except DoesNotExist:
            return None

    @classmethod
    def get_or_create(cls, id: str, **attrs) -> ChannelModel:
        return cls.get_or_none(str(id)) or cls.create(id, **attrs)

    @classmethod
    def update_or_none(cls, id: str, **attrs) -> Optional[ChannelModel]:
        try:
            instance = cls.get(str(id))
            instance.update_user(**attrs)
            return instance
        except DoesNotExist:
            return None

    @classmethod
    def update_or_create(cls, id: str, **attrs) -> ChannelModel:
        try:
            instance = cls.get(str(id))
            instance.update_user(**attrs)
            return instance
        except DoesNotExist:
            return cls.create(str(id), **attrs)

    def update_user(self, **attrs) -> bool:
        for attr, value in attrs.items():
            setattr(self, attr, value)
        self.save()
        return True

    def enable_command(self, command: str) -> bool:
        if command not in self.commands_disabled:
            return False
        self.commands_disabled.remove(command)
        self.save()
        return True

    def disable_command(self, command: str) -> bool:
        if command in self.commands_disabled:
            return False
        self.commands_disabled.append(command)
        self.save()
        return True

    def start(self) -> bool:
        if self.online:
            return False
        self.online = True
        self.save()
        return True

    def stop(self) -> bool:
        if not self.online:
            return False
        self.online = False
        self.save()
        return True
