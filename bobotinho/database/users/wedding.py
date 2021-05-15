# -*- coding: utf-8 -*-
from bobotinho.database.base import Base, TimestampMixin, fields


class Wedding(Base, TimestampMixin):
    user_1 = fields.ForeignKeyField("users.User", to_field="name", related_name="user_1")
    user_2 = fields.ForeignKeyField("users.User", to_field="name", related_name="user_2")
    divorced = fields.BooleanField(default=False)

    class Meta:
        app = "users"
        table = "wedding"
