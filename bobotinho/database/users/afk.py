# -*- coding: utf-8 -*-
from bobotinho.database.base import Base, TimestampMixin, ContentMixin, fields


class Afk(Base, TimestampMixin, ContentMixin):
    user = fields.ForeignKeyField("users.User", unique=True)
    alias = fields.CharField(max_length=8, null=True)

    class Meta:
        app = "users"
        table = "afk"
