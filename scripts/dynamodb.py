# -*- coding: utf-8 -*-
import os
import sys
from typing import Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bobotinho.models.channel import ChannelModel
from bobotinho.models.user import UserModel


def create_channel_table() -> Any:
    if not ChannelModel.exists():
        ChannelModel.create_table()
    return ChannelModel.describe_table()


def create_user_table() -> Any:
    if not UserModel.exists():
        UserModel.create_table()
    return UserModel.describe_table()


def add_channel(id, name, **attrs) -> dict[str, Any]:
    channel = ChannelModel.get(id)
    if not channel:
        channel = ChannelModel(id, name=name, **attrs)
        channel.save()
    return channel.attribute_values


def add_user(id, name, **attrs) -> dict[str, Any]:
    user = UserModel.get(id)
    if not user:
        user = UserModel(id, name=name, **attrs)
        user.save()
    return user.attribute_values


def all_channels() -> list[ChannelModel]:
    return ChannelModel.all()


def all_users() -> list[UserModel]:
    return UserModel.all()


if __name__ == "__main__":
    print(create_channel_table())
    print(create_user_table())
    print(add_channel("453651679", "discretinho"))
    print(add_user("453651679", "discretinho"))
    print(all_channels())
    print(all_users())
