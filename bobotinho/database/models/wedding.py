# -*- coding: utf-8 -*-
from bobotinho.database.base import Base, TimestampMixin, fields


class Wedding(Base, TimestampMixin):
    user_1 = fields.ForeignKeyField("models.Cookie", related_name="user_1")
    user_2 = fields.ForeignKeyField("models.Cookie", related_name="user_2")
    divorced = fields.BooleanField(default=False)

    class Meta:
        table = "wedding"