# -*- coding: utf-8 -*-
from bobotinho.database.base import Base, TimestampMixin, ContentMixin, fields


class Afk(Base, TimestampMixin, ContentMixin):
    user = fields.ForeignKeyField("users.User", to_field="name")
    alias = fields.CharField(max_length=8, null=True)
    status = fields.BooleanField(default=False)

    class Meta:
        app = "users"
        table = "afk"
